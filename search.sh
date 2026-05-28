#!/usr/bin/env bash
# Search OSINT tools by keyword
# Usage: ./search.sh <keyword>
#   ./search.sh github
#   ./search.sh "face recognition"
#   ./search.sh social | grep -i twitter

if [[ -z "$1" ]]; then
    echo "Usage: ./search.sh <keyword>"
    echo "       ./search.sh <keyword> --url       (URLs only)"
    echo "       ./search.sh <keyword> --category  (filter by category)"
    exit 1
fi

KEYWORD="$1"
MODE="$2"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CSV="$SCRIPT_DIR/data/tools-flat.csv"

if [[ "$MODE" == "--url" ]]; then
    grep -i "$KEYWORD" "$CSV" | cut -d',' -f3
elif [[ "$MODE" == "--category" ]]; then
    grep -i "$KEYWORD" "$CSV" | cut -d',' -f1 | sort -u
else
    # name | url | category
    awk -v kw="${KEYWORD,,}" -F',' '
        NR==1 { next }
        {
            row = tolower($0)
            if (index(row, kw)) {
                printf "%-35s %-50s %s\n", $2, $3, $1
            }
        }
    ' "$CSV"
fi
