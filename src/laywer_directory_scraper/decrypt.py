# Decrypt Email Address
# Ref: https://usamaejaz.com/cloudflare-email-decoding/#:~:text=You%20all%20know%20that%20Cloudflare,decode%20them%20on%20page%20load


def cfDecodeEmail(encodedString):
    r = int(encodedString[:2], 16)
    return "".join(
        chr(int(encodedString[i : i + 2], 16) ^ r) for i in range(2, len(encodedString), 2)
    )
