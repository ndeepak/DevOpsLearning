#!/usr/bin/env python3

import argparse
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

GITLAB_CA_CERT = os.getenv(
    "GITLAB_CA_CERT"
)

INPUT_FILE = "users_to_update.csv"

LOG_FILE = "email_migration_log.csv"

TIMEOUT = 30

API_URL = f"{GITLAB_URL}/api/v4"


HEADERS = {
    "PRIVATE-TOKEN": GITLAB_TOKEN,
    "Accept": "application/json",
}


# ============================================================
# TLS
# ============================================================

def get_verify_setting():

    if GITLAB_CA_CERT:

        if not os.path.isfile(
            GITLAB_CA_CERT
        ):

            print(
                f"ERROR: CA certificate not found: "
                f"{GITLAB_CA_CERT}"
            )

            sys.exit(1)

        return GITLAB_CA_CERT

    return True


VERIFY = get_verify_setting()


# ============================================================
# VALIDATION
# ============================================================

def validate_configuration():

    if not GITLAB_TOKEN:

        print(
            "ERROR: GITLAB_TOKEN is not set."
        )

        sys.exit(1)

    if not os.path.isfile(
        INPUT_FILE
    ):

        print(
            f"ERROR: {INPUT_FILE} not found."
        )

        sys.exit(1)


# ============================================================
# API REQUEST
# ============================================================

def api_request(
    method,
    endpoint,
    **kwargs
):

    url = f"{API_URL}{endpoint}"

    kwargs.setdefault(
        "headers",
        HEADERS
    )

    kwargs.setdefault(
        "timeout",
        TIMEOUT
    )

    kwargs.setdefault(
        "verify",
        VERIFY
    )

    try:

        return requests.request(
            method,
            url,
            **kwargs
        )

    except requests.exceptions.RequestException as e:

        print()
        print(
            f"REQUEST ERROR: {e}"
        )

        return None


# ============================================================
# GET USER
# ============================================================

def get_user(user_id):

    response = api_request(
        "GET",
        f"/users/{user_id}"
    )

    if response is None:
        return None

    if response.status_code != 200:

        print(
            f"ERROR getting user "
            f"{user_id}: "
            f"HTTP {response.status_code}"
        )

        print(response.text)

        return None

    return response.json()


# ============================================================
# GET USER EMAILS
# ============================================================

def get_user_emails(user_id):

    response = api_request(
        "GET",
        f"/users/{user_id}/emails"
    )

    if response is None:
        return None

    if response.status_code != 200:

        print(
            f"ERROR getting emails "
            f"for user {user_id}: "
            f"HTTP {response.status_code}"
        )

        print(response.text)

        return None

    return response.json()


# ============================================================
# ADD EMAIL
# ============================================================

def add_email(
    user_id,
    email
):

    response = api_request(
        "POST",
        f"/users/{user_id}/emails",
        data={
            "email": email,
            "skip_confirmation": "true",
        },
    )

    if response is None:
        return False

    if response.status_code == 201:

        print(
            "    New email added."
        )

        return True

    if response.status_code == 409:

        print(
            "    Email already exists."
        )

        return True

    print(
        f"    ERROR adding email: "
        f"HTTP {response.status_code}"
    )

    print(response.text)

    return False


# ============================================================
# MAKE PRIMARY
# ============================================================

def make_primary(
    user_id,
    email
):

    response = api_request(
        "PUT",
        f"/users/{user_id}",
        data={
            "email": email
        }
    )

    if response is None:
        return False

    if response.status_code == 200:

        print(
            "    New email is now primary."
        )

        return True

    print(
        f"    ERROR changing primary email: "
        f"HTTP {response.status_code}"
    )

    print(response.text)

    return False


# ============================================================
# VERIFY
# ============================================================

def verify(
    user_id,
    expected_email
):

    user = get_user(
        user_id
    )

    if user is None:
        return False

    actual_email = (
        user.get("email") or ""
    ).strip()

    if (
        actual_email.lower()
        ==
        expected_email.lower()
    ):

        print(
            f"    VERIFIED: {actual_email}"
        )

        return True

    print(
        "    VERIFICATION FAILED"
    )

    print(
        f"    Expected: {expected_email}"
    )

    print(
        f"    Actual:   {actual_email}"
    )

    return False


# ============================================================
# PROCESS USER
# ============================================================

def process_user(
    row,
    dry_run
):

    user_id = row["id"].strip()
    username = row["username"].strip()
    old_email = row["current_email"].strip()
    new_email = row["new_email"].strip()

    print()
    print("=" * 70)

    print(
        f"User ID : {user_id}"
    )

    print(
        f"Username: {username}"
    )

    print(
        f"Old     : {old_email}"
    )

    print(
        f"New     : {new_email}"
    )

    print("=" * 70)

    result = {

        "id": user_id,

        "username": username,

        "old_email": old_email,

        "new_email": new_email,

        "add_email": "NOT_RUN",

        "make_primary": "NOT_RUN",

        "verification": "NOT_RUN",

        "status": "UNKNOWN",
    }

    # --------------------------------------------------------
    # Validate CSV
    # --------------------------------------------------------

    if not user_id:
        result["status"] = "INVALID_USER_ID"
        return result

    if not new_email:
        result["status"] = "EMPTY_NEW_EMAIL"
        return result

    # --------------------------------------------------------
    # DRY RUN
    # --------------------------------------------------------

    if dry_run:

        print(
            "[DRY RUN] No changes will be made."
        )

        print(
            "    Would check current user."
        )

        print(
            "    Would add new email."
        )

        print(
            "    Would make new email primary."
        )

        print(
            "    Would verify."
        )

        result["status"] = "DRY_RUN"

        return result

    # --------------------------------------------------------
    # Get current user
    # --------------------------------------------------------

    user = get_user(
        user_id
    )

    if user is None:

        result["status"] = "FAILED_GET_USER"

        return result

    actual_email = (
        user.get("email") or ""
    ).strip()

    print(
        f"    GitLab current email: "
        f"{actual_email}"
    )

    # --------------------------------------------------------
    # IMPORTANT SAFETY CHECK
    # --------------------------------------------------------

    if (
        actual_email.lower()
        !=
        old_email.lower()
    ):

        print()
        print(
            "    STOPPED."
        )

        print(
            "    Current GitLab email "
            "does not match CSV."
        )

        print(
            f"    CSV    : {old_email}"
        )

        print(
            f"    GitLab : {actual_email}"
        )

        result["status"] = (
            "OLD_EMAIL_MISMATCH"
        )

        return result

    # --------------------------------------------------------
    # Check existing emails
    # --------------------------------------------------------

    emails = get_user_emails(
        user_id
    )

    if emails is None:

        result["status"] = (
            "FAILED_GET_EMAILS"
        )

        return result

    existing_emails = [

        (
            item.get("email") or ""
        ).lower()

        for item in emails
    ]

    # --------------------------------------------------------
    # Add new email if necessary
    # --------------------------------------------------------

    if new_email.lower() in existing_emails:

        print(
            "    Target email already "
            "exists on account."
        )

        result["add_email"] = (
            "ALREADY_EXISTS"
        )

    else:

        if not add_email(
            user_id,
            new_email
        ):

            result["add_email"] = (
                "FAILED"
            )

            result["status"] = (
                "FAILED_ADD_EMAIL"
            )

            return result

        result["add_email"] = (
            "SUCCESS"
        )

    # --------------------------------------------------------
    # Make primary
    # --------------------------------------------------------

    if not make_primary(
        user_id,
        new_email
    ):

        result["make_primary"] = (
            "FAILED"
        )

        result["status"] = (
            "FAILED_MAKE_PRIMARY"
        )

        return result

    result["make_primary"] = (
        "SUCCESS"
    )

    # --------------------------------------------------------
    # Verify
    # --------------------------------------------------------

    if verify(
        user_id,
        new_email
    ):

        result["verification"] = (
            "SUCCESS"
        )

        result["status"] = (
            "SUCCESS"
        )

    else:

        result["verification"] = (
            "FAILED"
        )

        result["status"] = (
            "VERIFICATION_FAILED"
        )

    return result


# ============================================================
# WRITE LOG
# ============================================================

def write_log(results):

    fieldnames = [

        "id",
        "username",
        "old_email",
        "new_email",
        "add_email",
        "make_primary",
        "verification",
        "status",
    ]

    with open(
        LOG_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(
            results
        )

    print()
    print(
        f"Log saved to: {LOG_FILE}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dry-run",
        action="store_true"
    )

    parser.add_argument(
        "--execute",
        action="store_true"
    )

    args = parser.parse_args()

    if (
        args.dry_run
        and
        args.execute
    ):

        print(
            "ERROR: Choose either "
            "--dry-run or --execute."
        )

        sys.exit(1)

    if (
        not args.dry_run
        and
        not args.execute
    ):

        print(
            "ERROR: Specify --dry-run "
            "or --execute."
        )

        print()

        print(
            "Example:"
        )

        print(
            "python3 update_gitlab_emails.py "
            "--dry-run"
        )

        print(
            "python3 update_gitlab_emails.py "
            "--execute"
        )

        sys.exit(1)

    validate_configuration()

    print("=" * 70)
    print("GitLab Email Update")
    print("=" * 70)

    print(
        f"GitLab URL: {GITLAB_URL}"
    )

    print(
        f"CSV       : {INPUT_FILE}"
    )

    print(
        "Mode      : "
        +
        (
            "DRY RUN"
            if args.dry_run
            else
            "EXECUTE"
        )
    )

    print("=" * 70)

    # --------------------------------------------------------
    # Read CSV
    # --------------------------------------------------------

    with open(
        INPUT_FILE,
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(
            file
        )

        rows = list(reader)

    print()
    print(
        f"Users loaded: {len(rows)}"
    )

    # --------------------------------------------------------
    # Process
    # --------------------------------------------------------

    results = []

    for row in rows:

        result = process_user(
            row,
            args.dry_run
        )

        results.append(
            result
        )

    # --------------------------------------------------------
    # Save log
    # --------------------------------------------------------

    write_log(
        results
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print(
        f"Total users: {len(results)}"
    )

    if args.dry_run:

        print(
            "Mode: DRY RUN"
        )

    else:

        successful = sum(
            1
            for r in results
            if r["status"] == "SUCCESS"
        )

        failed = len(results) - successful

        print(
            f"Successful: {successful}"
        )

        print(
            f"Failed:     {failed}"
        )

    print("=" * 70)


if __name__ == "__main__":
    main()