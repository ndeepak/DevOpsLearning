#!/usr/bin/env python3

import csv
import os
import sys
import requests


# ============================================================
# CONFIGURATION
# ============================================================

GITLAB_URL = os.getenv(
    "GITLAB_URL",
    "https://gitlabuat.com"
).rstrip("/")

GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")

# Optional internal CA certificate
GITLAB_CA_CERT = os.getenv("GITLAB_CA_CERT")

SOURCE_DOMAIN = "@cas.com.np"
SUGGESTED_TARGET_DOMAIN = "@castotal.com"

ALL_USERS_FILE = "all_gitlab_users.csv"
USERS_TO_UPDATE_FILE = "users_to_update.csv"

PER_PAGE = 100
TIMEOUT = 30

API_URL = f"{GITLAB_URL}/api/v4"


# ============================================================
# HEADERS
# ============================================================

HEADERS = {
    "PRIVATE-TOKEN": GITLAB_TOKEN,
    "Accept": "application/json",
}


# ============================================================
# VALIDATION
# ============================================================

def validate_configuration():

    if not GITLAB_TOKEN:

        print("ERROR: GITLAB_TOKEN is not set.")

        print()
        print("Set it with:")
        print(
            'export GITLAB_TOKEN="YOUR_ADMIN_TOKEN"'
        )

        sys.exit(1)


# ============================================================
# TLS
# ============================================================

def get_verify_setting():

    if GITLAB_CA_CERT:

        if not os.path.isfile(GITLAB_CA_CERT):

            print(
                f"ERROR: CA certificate not found: "
                f"{GITLAB_CA_CERT}"
            )

            sys.exit(1)

        return GITLAB_CA_CERT

    return True


VERIFY = get_verify_setting()


# ============================================================
# GET ALL USERS
# ============================================================

def get_all_users():

    users = []

    url = f"{API_URL}/users"

    params = {
        "pagination": "keyset",
        "per_page": PER_PAGE,
        "order_by": "id",
        "sort": "asc",
    }

    while url:

        print()
        print(f"Requesting: {url}")

        try:

            response = requests.get(
                url,
                headers=HEADERS,
                params=params,
                timeout=TIMEOUT,
                verify=VERIFY,
            )

        except requests.exceptions.RequestException as e:

            print()
            print("ERROR connecting to GitLab:")
            print(e)

            sys.exit(1)

        if response.status_code != 200:

            print()
            print(
                f"ERROR: GitLab returned "
                f"HTTP {response.status_code}"
            )

            print(response.text)

            sys.exit(1)

        batch = response.json()

        if not batch:
            break

        users.extend(batch)

        print(
            f"Received {len(batch)} users "
            f"(total: {len(users)})"
        )

        # ----------------------------------------------------
        # Keyset pagination
        # ----------------------------------------------------

        link_header = response.headers.get("Link")

        next_url = None

        if link_header:

            for link in link_header.split(","):

                if 'rel="next"' in link:

                    next_url = (
                        link
                        .split(";")[0]
                        .strip()
                    )

                    if (
                        next_url.startswith("<")
                        and
                        next_url.endswith(">")
                    ):

                        next_url = next_url[1:-1]

                    break

        url = next_url

        # The next URL already contains its parameters.
        params = None

    return users


# ============================================================
# SAVE ALL USERS
# ============================================================

def save_all_users(users):

    fieldnames = [
        "id",
        "username",
        "name",
        "email",
        "state",
        "is_admin",
        "external",
        "blocked",
    ]

    with open(
        ALL_USERS_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for user in users:

            writer.writerow({
                "id": user.get("id", ""),
                "username": user.get("username", ""),
                "name": user.get("name", ""),
                "email": user.get("email") or "",
                "state": user.get("state", ""),
                "is_admin": user.get("is_admin", ""),
                "external": user.get("external", ""),
                "blocked": user.get("blocked", ""),
            })

    print()
    print(
        f"Saved all users to: {ALL_USERS_FILE}"
    )


# ============================================================
# CREATE USERS TO UPDATE
# ============================================================

def create_users_to_update(users):

    target_users = []

    for user in users:

        email = (
            user.get("email") or ""
        ).strip()

        state = (
            user.get("state") or ""
        ).lower()

        # ----------------------------------------------------
        # Only active users
        # ----------------------------------------------------

        if state != "active":
            continue

        # ----------------------------------------------------
        # Only @cas.com.np
        # ----------------------------------------------------

        if not email.lower().endswith(
            SOURCE_DOMAIN
        ):
            continue

        # ----------------------------------------------------
        # Generate suggested email
        # ----------------------------------------------------

        local_part = email[
            :-len(SOURCE_DOMAIN)
        ]

        suggested_email = (
            local_part
            + SUGGESTED_TARGET_DOMAIN
        )

        target_users.append({

            "id": user.get("id", ""),

            "username": user.get(
                "username",
                ""
            ),

            "name": user.get(
                "name",
                ""
            ),

            "current_email": email,

            "new_email": suggested_email,

            "state": state,

            "is_admin": user.get(
                "is_admin",
                False
            ),
        })

    return target_users


# ============================================================
# SAVE USERS TO UPDATE
# ============================================================

def save_users_to_update(users):

    fieldnames = [
        "id",
        "username",
        "name",
        "current_email",
        "new_email",
        "state",
        "is_admin",
    ]

    with open(
        USERS_TO_UPDATE_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        writer.writerows(users)

    print(
        f"Saved migration candidates to: "
        f"{USERS_TO_UPDATE_FILE}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    validate_configuration()

    print("=" * 70)
    print("GitLab User Extraction")
    print("=" * 70)

    print(
        f"GitLab URL       : {GITLAB_URL}"
    )

    print(
        f"Source domain    : {SOURCE_DOMAIN}"
    )

    print(
        f"Suggested domain : {SUGGESTED_TARGET_DOMAIN}"
    )

    print("=" * 70)

    # --------------------------------------------------------
    # Extract
    # --------------------------------------------------------

    users = get_all_users()

    print()
    print(
        f"Total users found: {len(users)}"
    )

    # --------------------------------------------------------
    # Save everything
    # --------------------------------------------------------

    save_all_users(users)

    # --------------------------------------------------------
    # Filter
    # --------------------------------------------------------

    target_users = create_users_to_update(
        users
    )

    print()
    print(
        f"Active users with "
        f"{SOURCE_DOMAIN}: "
        f"{len(target_users)}"
    )

    # --------------------------------------------------------
    # Save candidates
    # --------------------------------------------------------

    save_users_to_update(
        target_users
    )

    # --------------------------------------------------------
    # Preview
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("USERS TO REVIEW")
    print("=" * 70)

    for user in target_users:

        print(
            f"{user['id']:>6} | "
            f"{user['username']:<30} | "
            f"{user['current_email']:<40} -> "
            f"{user['new_email']}"
        )

    print()
    print("=" * 70)
    print("IMPORTANT")
    print("=" * 70)

    print(
        "Review users_to_update.csv before running "
        "the update script."
    )

    print(
        "You can change the new_email column "
        "according to your email policy."
    )

    print(
        "This script does NOT modify GitLab."
    )

    print("=" * 70)


if __name__ == "__main__":
    main()