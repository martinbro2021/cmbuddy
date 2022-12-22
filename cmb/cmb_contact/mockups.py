SNIPPET_MOCKUP = {
    "contact_title": "Contact",
    "contact_success_title": "Message sent",
}

LINK_MOCKUP = {}

CONTACTCONTENT_MOCKUP = {
    "contact-header":  # keys don't matter here. you just need a *different* key for each value
    {
        "html":
            '<p>&nbsp;</p>'
            '<h1 style = "text-align: center"> Thank you </h1>',

        "position": 10,
        "reference": "/contact/success",
    },
    "contact-msg-received":
    {
        "html":
            '<hr/>'
            '<p style="text-align: center">I received your message. I will reply soon.</p>',

        "position": 20,
        "reference": "/contact/success",
    },
    "contact-me":
    {
        "html":
            '<p>&nbsp;</p>'
            '<h1 style = "text-align: center">Contact Me</h1>',

        "position": 10,
        "reference": "/contact",
    },
    "contact-invitation":
    {
        "html":
        '<hr/><p>Leave a greeting or ask me a question</p>',

        "position": 20,
        "reference": "/contact",
    },
    "contact-legal-info":
    {
        "html":
        '<p>Please note the '
        '<a title="legal information" href="https://www.example.com" target="_blank" rel="noopener">'
        'privacy policy</a>'
        '</p>',
        "position": 30,
        "reference": "/contact"
    },
}

SETTING_MOCKUP = {
    "contact_email_recipients": "me@example.com, you@example.com"
}
