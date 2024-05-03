<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Customer Support Bot</h3>

  <p align="center">
    A web app that allows anyone to get customized customer support ai chatbots for their business in minutes!
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    ·
    <a href="https://github.com/imadahmad97/customer-support-bot/issues/new">Report Bug</a>

  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>
```
customer-support-bot
├─ .gcloudignore
├─ .git
│  ├─ COMMIT_EDITMSG
│  ├─ FETCH_HEAD
│  ├─ HEAD
│  ├─ ORIG_HEAD
│  ├─ config
│  ├─ description
│  ├─ hooks
│  │  ├─ applypatch-msg.sample
│  │  ├─ commit-msg.sample
│  │  ├─ fsmonitor-watchman.sample
│  │  ├─ post-update.sample
│  │  ├─ pre-applypatch.sample
│  │  ├─ pre-commit.sample
│  │  ├─ pre-merge-commit.sample
│  │  ├─ pre-push.sample
│  │  ├─ pre-rebase.sample
│  │  ├─ pre-receive.sample
│  │  ├─ prepare-commit-msg.sample
│  │  ├─ push-to-checkout.sample
│  │  ├─ sendemail-validate.sample
│  │  └─ update.sample
│  ├─ index
│  ├─ info
│  │  └─ exclude
│  ├─ logs
│  │  ├─ HEAD
│  │  └─ refs
│  │     ├─ heads
│  │     │  └─ main
│  │     └─ remotes
│  │        └─ origin
│  │           ├─ HEAD
│  │           └─ main
│  ├─ objects
│  │  ├─ 0d
│  │  │  └─ 3f03aff9941d3be51cf579c5f1160a4c358cde
│  │  ├─ 23
│  │  │  └─ d66f3dea2e9808541f175c6bba44133373c839
│  │  ├─ 41
│  │  │  └─ 113400ac5f1c1d3eba0e2412e8d61bcb1153a6
│  │  ├─ 49
│  │  │  └─ 5c0ea8d0afab91f6fbbe7e7c266c09ec52a156
│  │  ├─ 4c
│  │  │  └─ 6cac440c64ed4773487b314482ea21da42f29d
│  │  ├─ 5e
│  │  │  ├─ 2aee997846fbc80013f90b5b343a8ebf183ea2
│  │  │  └─ 4d20f0b70556dcd01005d640e5d6955a464dec
│  │  ├─ 64
│  │  │  └─ f65b00750d6d1892a542447fe5048b59a07d9b
│  │  ├─ 6d
│  │  │  └─ a7481bfe6bd99dbd5d084540aaef5f14f61739
│  │  ├─ 89
│  │  │  └─ d2ddaa9476ac4049b1717be0e538eb52b63071
│  │  ├─ 8e
│  │  │  └─ 3e56d6c6213f9d2dae508251d451ab2837e4db
│  │  ├─ 96
│  │  │  └─ bec4efb50ab3416d7a7bd4c1ba9e8482f11ee0
│  │  ├─ 9c
│  │  │  └─ 7a8f94711451bfc72a8d07ab91a9625ba96b90
│  │  ├─ 9d
│  │  │  └─ a7f6c1f67759a7d33aa22b90a18ec1ec23acd0
│  │  ├─ ba
│  │  │  └─ afac615a39f88b3d6135801df59a9b042b69d1
│  │  ├─ cc
│  │  │  └─ c08fc86cb8bfe77e86a951a2ee05ca627153ea
│  │  ├─ ce
│  │  │  └─ a6e8778ecc8fc88b71df672806cb1dcfe28215
│  │  ├─ d1
│  │  │  └─ 5106d7fc5c62170e08d2bd0b16c1622297ff27
│  │  ├─ da
│  │  │  └─ c3dea29c63fc53ff106080a2da16a05c80d2a5
│  │  ├─ fe
│  │  │  └─ a51147dc910cc00fc8b7d546e4998624e06cab
│  │  ├─ info
│  │  └─ pack
│  │     ├─ pack-10ecaccc27ddec0821e2a29ccd13aa052db566cf.idx
│  │     ├─ pack-10ecaccc27ddec0821e2a29ccd13aa052db566cf.pack
│  │     └─ pack-10ecaccc27ddec0821e2a29ccd13aa052db566cf.rev
│  ├─ packed-refs
│  └─ refs
│     ├─ heads
│     │  └─ main
│     ├─ remotes
│     │  └─ origin
│     │     ├─ HEAD
│     │     └─ main
│     └─ tags
├─ .gitignore
├─ README.md
├─ app
│  ├─ __init__.py
│  ├─ config.py
│  ├─ extensions.py
│  ├─ models.py
│  ├─ routes.py
│  ├─ static
│  │  ├─ bots.css
│  │  ├─ create_chatbot.css
│  │  ├─ header.css
│  │  ├─ images
│  │  │  ├─ cta-illustration.svg
│  │  │  ├─ feature-icon-01.svg
│  │  │  ├─ feature-icon-02.svg
│  │  │  ├─ feature-icon-03.svg
│  │  │  ├─ feature-icon-04.svg
│  │  │  ├─ feature-icon-05.svg
│  │  │  ├─ feature-icon-06.svg
│  │  │  ├─ hero-back-illustration.svg
│  │  │  ├─ hero-top-illustration.svg
│  │  │  ├─ logo.svg
│  │  │  └─ pricing-illustration.svg
│  │  ├─ index.css
│  │  ├─ login.css
│  │  ├─ login.js
│  │  ├─ main.min.js
│  │  ├─ post_registration.css
│  │  ├─ questions.css
│  │  ├─ questions.js
│  │  └─ style.css
│  ├─ templates
│  │  ├─ bots.html
│  │  ├─ chat.html
│  │  ├─ chat_preview.html
│  │  ├─ confirm_email.html
│  │  ├─ create_chatbot.html
│  │  ├─ header.html
│  │  ├─ index.html
│  │  ├─ layout.html
│  │  ├─ login.html
│  │  ├─ post_registration.html
│  │  ├─ public_chat.html
│  │  └─ register.html
│  ├─ token.py
│  └─ utils.py
├─ app.yaml
└─ run.py

```