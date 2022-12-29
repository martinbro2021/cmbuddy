import logging
from base64 import b64encode
from hashlib import sha256
from random import Random
from time import time
from uuid import uuid4

from captcha.image import ImageCaptcha

rnd = Random()
logger = logging.getLogger(__name__)


class ProofOfWorkException(Exception):
    """Indicates that the calculated POW does not meet the requirements."""


class CMBCaptcha:

    def __init__(self, digits: int, lifespan: int, pool: str, proof_of_work_difficulty: int) -> None:
        self.valid_captchas = {}
        self.digits = digits
        self.lifespan = lifespan
        self.pool = pool
        self.leading_zeros = "0" * proof_of_work_difficulty
        self.difficulty = proof_of_work_difficulty

    def create_captcha(self) -> dict:
        """Creates a base 64 encoded image containing a captcha."""
        self.clean_up()
        rnd_str = "".join(rnd.choice(self.pool) for _ in range(self.digits))
        with ImageCaptcha().generate(rnd_str) as bytes:
            img = b64encode(bytes.read()).decode("utf-8")
        uuid = uuid4()
        self.valid_captchas.update(
            {uuid.int: (hash(rnd_str), int(time()))})
        return {
            "img": img,
            "uuid": str(uuid),
            "difficulty": self.difficulty,
            "digits": self.digits
        }

    def is_valid(self, uuid: int, captcha: int, msg: str, pow: str) -> bool:
        """
        Returns true if the captcha has been entered correctly and the proof of work meets the requirements.
        Raises a ProofOfWorkException if the pow doesn't meet the requirements.
        """
        self.clean_up()
        if uuid in self.valid_captchas:
            valid_captcha = self.valid_captchas.pop(uuid)[0]
            self.check_proof_of_work(msg, pow)
            return captcha == valid_captcha
        return False

    def check_proof_of_work(self, msg: str, pow: str) -> None:
        """
        Checks if the hash of (msg+pow) starts with the number of zeros that is stated by
        proof_of_work_difficulty.
        """
        sha = sha256((pow + msg).encode("utf-8")).hexdigest()
        if not sha.startswith(self.leading_zeros):
            logger.info(f"pow:{pow}/msg:{msg}/sha:{sha} - the value does not meet the requirements.")
            raise ProofOfWorkException(f"The sha256 must start with at least {self.difficulty} zeros")

    def clean_up(self):
        """Invalidates (=deletes) all captchas that have exceeded their lifetime"""
        t = time()
        to_pop = []
        for key, value in self.valid_captchas.items():
            if t - value[1] > self.lifespan:
                to_pop.append(key)
        for key in to_pop:
            self.valid_captchas.pop(key)
        logger.debug(f"Deleted {len(to_pop)} captchas. Valid captchas: {len(self.valid_captchas)}")
