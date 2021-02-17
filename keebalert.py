# Imports
import argparse
import scraper
import formatter
import notify


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--interest-check",
        dest="ic",
        action='store_true',
        help="Enable Interest Checks"
    )
    parser.add_argument(
        "-g",
        "--group-buy",
        dest="gb",
        action='store_true',
        help="Enable Group Buys"
    )
    parser.add_argument(
        "-s",
        "--sms",
        dest="sms",
        action='store_true',
        help="Send via SMS"
    )
    parser.add_argument(
        "-e",
        "--email",
        dest="email",
        action='store_true',
        help="Send via Email"
    )
    parser.add_argument(
        "-ep",
        "--port",
        dest="port",
        help="Email Port"
    )
    parser.add_argument(
        "-ef",
        "--email-from",
        dest="email_from",
        help="Sender Email Address"
    )
    parser.add_argument(
        "-et",
        "--email-to",
        dest="email_to",
        help="Recipient Email Address"
    )
    parser.add_argument(
        "-p",
        "--email-pass",
        dest="email_pass",
        help="Email Pass"
    )
    parser.add_argument(
        "-es",
        "--email-server",
        dest="email_server",
        help="Email Server"
    )
    parser.add_argument(
        "--ti",
        "--twilio-id",
        dest="twilio_id",
        help="SMS Id"
    )
    parser.add_argument(
        "-tk",
        "--twilio-key",
        dest="twilio_key",
        help="SMS Key"
    )
    parser.add_argument(
        "-sf",
        "--sms-from",
        dest="sms_from",
        help="Sender Phone Number"
    )
    parser.add_argument(
        "-st",
        "--sms-to",
        dest="sms_to",
        help="SMS Recipient Phone Number"
    )

    args = parser.parse_args()

    # Ensure that the parameters passed are valid
    if args.email and (not args.email_from or not args.email_to or not args.email_pass or not args.email_server or not args.port):
        parser.error("--email requires --email-to, --email-from, --email-pass, --email-server, and --port")
    
    if args.sms and (not args.sms_from or not args.sms_to or not args.twilio_id or not args.twilio_key):
        parser.error("--sms requires --sms-to, --sms-from, --twilio-id, and --twilio-key")

    # Scrapes the selected forums and returns dictionaries. Returned values may be None
    gb_dict,ic_dict = scraper.main(ic=args.ic, gb=args.gb)

    if args.email:
        email_message = formatter.email(ic_dict=ic_dict, gb_dict=gb_dict)
        notify.email(message=email_message, email_to=email_to, email_from=email_from, email_pass=email_pass, email_server=email_server, port=port)

    if args.sms:
        sms_message = formatter.sms(ic_dict=ic_dict, gb_dict=gb_dict)
        notify.sms(message=sms_message, sms_to=sms_to, sms_from=sms_from, twilio_id=twilio_id, twilio_key=twilio_key)


if __name__ == "__main__":
    main()
