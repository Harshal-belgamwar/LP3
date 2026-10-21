
from email import policy
from email.parser import Parser
from email.utils import parseaddr
import re


def analyze_email_header():
    print("=" * 45)
    print("       EMAIL HEADER ANALYZER")
    print("=" * 45)
    print("Paste the complete email header below.")
    print("Type END on a separate line when finished.\n")

    # Step 1: Read headers from terminal
    lines = []

    while True:
        try:
            line = input()
        except EOFError:
            print("\nInput ended.")
            return

        if line.strip().upper() == "END":
            break

        lines.append(line)

    header_text = "\n".join(lines).strip()

    # Step 2: Debug input
    print("\nDEBUG: Characters received:", len(header_text))

    if not header_text:
        print("ERROR: No email header was entered.")
        return

    # Step 3: Parse email headers
    msg = Parser(policy=policy.default).parsestr(header_text)

    # Step 4: Display basic email information
    print("\n===== EMAIL ANALYSIS REPORT =====")
    print("From:", msg.get("From", "Not available"))
    print("To:", msg.get("To", "Not available"))
    print("Subject:", msg.get("Subject", "Not available"))
    print("Date:", msg.get("Date", "Not available"))
    print("Reply-To:", msg.get("Reply-To", "Not available"))
    print("Message-ID:", msg.get("Message-ID", "Not available"))

    # Step 5: Routing information and IPv4 addresses
    received_headers = msg.get_all("Received", [])

    print("\n===== EMAIL ROUTING INFORMATION =====")

    if received_headers:
        for i, received in enumerate(received_headers, 1):
            print(f"\nHop {i}:")
            print(received)

            ips = re.findall(
                r'(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])',
                str(received)
            )

            for ip in ips:
                octets = ip.split(".")

                if all(0 <= int(octet) <= 255 for octet in octets):
                    print("IP Address:", ip)
    else:
        print("No Received headers found.")

    # Step 6: Check suspicious indicators
    print("\n===== SUSPICIOUS INDICATORS =====")

    from_addr = parseaddr(str(msg.get("From", "")))[1].lower()
    reply_to = parseaddr(str(msg.get("Reply-To", "")))[1].lower()

    if from_addr and reply_to:
        if from_addr != reply_to:
            print("Warning: Reply-To differs from From.")
        else:
            print("Reply-To matches From.")
    else:
        print("From/Reply-To comparison unavailable.")

    auth_results = str(
        msg.get("Authentication-Results", "")
    ).lower()

    if auth_results:
        print("Authentication-Results:", auth_results)
    else:
        print("Authentication-Results header not found.")

    # Step 7: Rule-based spam detection
    print("\n===== SPAM DETECTION =====")

    spam_score = 0
    reasons = []

    # Rule 1: Reply-To address differs from From address
    if from_addr and reply_to and from_addr != reply_to:
        spam_score += 1
        reasons.append("Reply-To differs from From address.")

    # Rule 2: Suspicious subject keywords
    subject = str(msg.get("Subject", "")).lower()

    suspicious_keywords = [
        "urgent",
        "verify your account",
        "click here",
        "password",
        "account suspended",
        "claim your prize",
        "free money",
        "limited time",
        "immediately"
    ]

    matched_keywords = [
        word for word in suspicious_keywords
        if word in subject
    ]

    if matched_keywords:
        spam_score += 1
        reasons.append(
            "Suspicious subject keywords: "
            + ", ".join(matched_keywords)
        )

    # Rule 3: Failed SPF, DKIM, and DMARC checks
    for method in ["spf", "dkim", "dmarc"]:
        pattern = r"\b" + method + r"\s*=\s*fail\b"

        if re.search(pattern, auth_results):
            spam_score += 1
            reasons.append(method.upper() + " authentication failed.")

    # Step 8: Display the final result
    if reasons:
        print("\nSuspicious indicators found:")

        for reason in reasons:
            print("-", reason)
    else:
        print("No suspicious indicators found by these rules.")

    print("\nSpam Score:", spam_score, "/ 5")

    if spam_score >= 3:
        print("Final Result: LIKELY SPAM")
    else:
        print("Final Result: NO STRONG SPAM INDICATORS DETECTED")

    print("\nAnalysis completed.")


if __name__ == "__main__":
    analyze_email_header()
