from cmb_captcha.cmb_captcha import CMBCaptcha

POOL = "ABCDEFGHJKLMNPQRSTUVWXYZ2345689"  # avoid ambiguous characters like 0 <-> O, 1 <-> I, X <-> x, 7 <-> 1
DIFFICULTY = 4  # difficulty of the proof-of-work - number of leading zeros
DIGITS = 5  # number of digits of the captcha
LIFESPAN = 600  # lifespan of a captcha in seconds

cmb_captcha = CMBCaptcha(DIGITS, LIFESPAN, POOL, DIFFICULTY)


def get_context() -> dict:
    return {"captcha": cmb_captcha.create_captcha()}


def is_valid_captcha(post: dict) -> bool:
    uuid = int(post["uuid"].replace("-", ""), base=16)
    captcha = hash(post["captcha"].upper())
    pow = post["pow"]
    msg_fields = ("name", "email", "subject", "message", "captcha")
    msg = "".join([post[field] for field in msg_fields])
    return cmb_captcha.is_valid(uuid, captcha, msg, pow)
