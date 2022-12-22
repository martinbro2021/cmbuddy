SNIPPET_MOCKUP = {
    "contact_title": "Contact",
    "contact_success_title": "Message sent",
}

LINK_MOCKUP = {}

CONTACT_CONTENT_MOCKUP = {
    "contact-header":
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
        '<p>'
        '<a title="Privacy Policy and Legal Notices" href="https://www.example.com" target="_blank" rel="noopener">'
        'Privacy Policy and Legal Notices</a>'
        '</p>',
        "position": 30,
        "reference": "/contact"
    },
}

SETTING_MOCKUP = {
    "contact_email_recipients": "me@example.com, you@example.com"
}


MENU_ENTRY_MOCKUP = {
    "Contact":
    {
        "name": "Contact",
        "url": "/contact",
        "position": 20
    }
}
