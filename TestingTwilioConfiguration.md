### Sending message with multimedia content.

curl -X POST https://api.twilio.com/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Messages.json \
--data-urlencode "To=whatsapp:+13105555555" \
--data-urlencode "From=whatsapp:+12125551234" \
--data-urlencode "Body=Thanks for contacting me on WhatsApp! Here is a picture of an owl." \
--data-urlencode “MediaUrl=https://demo.twilio.com/owl.png” \
-u "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX:your_auth_token"

For send any media content just add the link to media content using "MediaUrl=[link to content]"
More documentation in: https://www.twilio.com/blog/whatsapp-media-support

