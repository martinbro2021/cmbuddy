/**
 * Provides proof-of-work functionality
 */
let pow = {
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

/**
 * Methods for handling the contact form.
 */
let cForm = {
  /**
   * Client-side check if the form is valid. Generates proof of work
   * and submits form if the form is valid.
   */
  onSubmit: function (btn, difficulty) {
    const form = document.getElementById("contact-form");
    if (!this.isValid(form)) {
      return;
    }

    this.styleForm(btn, form);

    pow.generate(this.createMsg(form), difficulty).then((nonce) => {
      document.getElementById("pow").setAttribute("value", nonce);
      console.debug("NONCE:", nonce);
      form.submit();
    });
  },

  /**
   * Returns true if the requirements for the input fields of the form
   * are satisfied.
   */
  isValid: function (form) {
    if (!form.checkValidity()) {
      if (form.reportValidity) {
        form.reportValidity();
        return false;
      }
    }
    return true;
  },

  /**
   * Compiles the message with all fields that are relevant to the proof of work.
   */
  createMsg: function (form) {
    let msg = "";
    const powRelevant = form.getElementsByClassName("_pow_relevant");
    for (let elem of powRelevant) {
      msg += elem.value;
    }
    return msg;
  },

  /**
   * Disables submit button, adds spinner.
   */
  styleForm(btn, form) {
    btn.setAttribute("disabled", "");
    this.addSpinner(form);
  },

  /**
   * Adds spinner to all input fields within the form that are relevant
   * for the proof of work.
   */
  addSpinner: function (form) {
    form.style.cursor = "wait";
    const inputFields = form.getElementsByClassName("_pow_relevant");
    for (let inputField of inputFields) {
      inputField.style.cursor = "wait";
      inputField.setAttribute("readonly", "");
    }
  },
};
