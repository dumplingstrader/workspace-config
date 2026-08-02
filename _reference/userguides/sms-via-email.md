# Sending SMS via Email (Carrier Email-to-SMS Gateways)

## Solution Concept

To send a text message via email, you must use an SMS or MMS "email gateway" address provided by the recipient's carrier.

In general, the method is to replace the carrier's gateway address with the recipient's 10-digit cell number, in the format:

```
number@cell_provider_domain.com
```

**Example (USA, AT&T):** to text an AT&T user, send an email to `2001234567@txt.att.net`, where `200` is the area code and `123-4567` is the cell number.

This is the easiest way to send an SMS without a dedicated texting app or service -- just send a regular email to the right address.

## USA Carrier Gateway List

| Carrier | SMS Gateway | MMS Gateway |
|---|---|---|
| AT&T | number@txt.att.net | number@mms.att.net |
| T-Mobile | number@tmomail.net | number@tmomail.net |
| Verizon | number@vtext.com | number@vzwpix.com |
| Sprint | number@messaging.sprintpcs.com | number@pm.sprint.com |
| Xfinity Mobile | number@vtext.com | number@mypixmessages.com |
| Virgin Mobile | number@vmobl.com | number@vmpix.com |
| Tracfone | -- | number@mmst5.tracfone.com |
| Simple Mobile | number@smtext.com | -- |
| Mint Mobile | number@mailmymobile.net | -- |
| Red Pocket | number@vtext.com | -- |
| Metro PCS | number@mymetropcs.com | number@mymetropcs.com |
| Boost Mobile | number@sms.myboostmobile.com | number@myboostmobile.com |
| Cricket | number@sms.cricketwireless.net | number@mms.cricketwireless.net |
| Republic Wireless | number@text.republicwireless.com | -- |
| Google Fi (Project Fi) | number@msg.fi.google.com | number@msg.fi.google.com |
| U.S. Cellular | number@email.uscc.net | number@mms.uscc.net |
| Ting | number@message.ting.com | -- |
| Consumer Cellular | number@mailmymobile.net | -- |
| C-Spire | number@cspire1.com | -- |
| Page Plus | number@vtext.com | -- |

*Note: "number" = the recipient's 10-digit phone number (area code + local number), no dashes or spaces.*

For carriers outside the USA, check the local provider's documentation for their email-to-SMS gateway address.

## Caveats

- The recipient's carrier must be known and correctly matched -- sending to the wrong gateway domain will fail silently or bounce.
- Many carriers rate-limit or block gateway messages if they look like spam (links, images, bulk sending).
- Some carriers have discontinued or restricted their email-to-SMS gateways over time, so addresses should be verified before relying on them for production use.

## Source

Screenshots: `sms1.png`, `sms2.png` (this folder).
