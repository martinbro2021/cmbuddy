/**
 * Provides proof-of-work functionalities
 */
var pow = {
  /**
   * Calculates a nonce so that the hex representation of
   * sha256(nonce + msg) starts with the given number of zeros
   */
  generate: async function (msg, leading_zeros) {
    const zeros_even = Math.floor(leading_zeros / 2);
    let nonce = 0;
    let checksum = 1;
    while (checksum != 0) {
      nonce++;
      const encoded = new TextEncoder().encode(nonce + msg);
      const buffer = await crypto.subtle.digest("SHA-256", encoded);
      array = Array.from(new Uint8Array(buffer));
      checksum = 0;
      for (let i = 0; i < zeros_even; i++) {
        checksum += array[i];
      }
      if (leading_zeros % 2) {
        const temp = array[zeros_even];
        checksum += temp < 16 ? 0 : temp;
      }
    }
    return nonce;
  },
};

var cForm = {
  onSubmit: function (btn, difficulty) {
    const form = get("contact-form");
    if (!this.isValid(form)) {
      return;
    }

    this.styleForm(btn, form);

    pow.generate(this.createMsg(form), difficulty).then((nonce) => {
      get("pow").setAttribute("value", nonce);
      console.debug("NONCE:", nonce);
      form.submit();
    });
  },

  isValid: function (form) {
    if (!form.checkValidity()) {
      if (form.reportValidity) {
        form.reportValidity();
        return false;
      }
    }
    return true;
  },

  createMsg: function (form) {
    let msg = "";
    const powRelevant = form.getElementsByClassName("_pow_relevant");
    for (let elem of powRelevant) {
      msg += elem.value;
    }
    return msg;
  },

  styleForm(btn, form) {
    btn.setAttribute("disabled", "");
    this.addSpinner(form);
  },

  addSpinner: function (form) {
    form.style.cursor = "wait";
    const inputFields = form.getElementsByClassName("_pow_relevant");
    for (let inputField of inputFields) {
      inputField.style.cursor = "wait";
      inputField.setAttribute("readonly", "");
    }
  },
};

/**
 * document.getElementById convenience wrapper
 */
let get = function (elem) {
  return document.getElementById(elem);
};

/**
 * document.getElementById(elem).value convenience wrapper
 */
let val = function (elem) {
  return document.getElementById(elem).value;
};
