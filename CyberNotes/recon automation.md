# Recon automation


```bash
export TARGET="example.com"
```

## Phase 1: Subdomain Enum

```bash
subfinder -d $TARGET -silent | anew subdomains.txt
```

Pro tip: Add API keys to ~/.config/subfinder/provider-config.yaml for 10x more results. Even free API keys for VirusTotal and SecurityTrails make a huge difference.


### The certificate transparency goldmine

```bash
curl -s "https://crt.sh/?q=%25.$TARGET&output=json" | jq -r '.[].name_value' | sed 's/\*\.//g' | sort -u | anew subdomains.txt
```

What it does: Hits crt.sh (the certificate transparency log database), pulls every SSL certificate ever issued for your target domain, extracts subdomain names, removes wildcards (*.), deduplicates, and saves.
**Why it works:** Companies can't hide SSL certificates. Every time they spin up a new subdomain with HTTPS, a record gets logged in the public CT logs _forever_. This catches subdomains that passive DNS tools miss entirely — especially old staging servers and forgotten apps.

### Assetfinder + deduplication combo
```bash
assetfinder --subs-only $TARGET | sort -u | anew subdomains.txt
```

### find juicy subdomains using filter
```bash
cat subdomains.txt | grep --color -E 'api|dev|stg|test|admin|demo|stage|pre|vpn|internal|beta|uat|backup|old|legacy'
```

### live subdomain checker
```bash
cat subdomains.txt | httpx -silent -o live_hosts.txt
```

### tech fingerprinting
```bash
cat live_hosts.txt | httpx -silent -title -tech-detect -status-code -content-length
```

### subdomain takeover scanner
```bash
subjack -w subdomains.txt -t 100 -timeout 30 -ssl -c ~/go/pkg/mod/github.com/haccer/subjack*/fingerprints.json -v
```


## Phase 2 
