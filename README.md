<div align="center">
    <img src="assets/thumbnail.png" width="350">
</div>

<h1 align="center">The open-source limit-free file-sharing tool</h1>

Host and share your local file globally, control the sharing proccess and there is no limit to the sharing times or file size; Where there is no third-party services involved, only you and your file (XoX#)!.

<div align="center">
    <img src="assets/preview.png" width=800em>
</div>

- ✋ **No third-party services** - Because it's not using any third-party services, it's 100% free of cost and limits.
- 🔒 **You in control** - You control the sharing permissions. You can prevent and deny any request for accessing your file in real-time. Or even, just allow everyone to download it.
- 😌 **Easy-to-use** - The UI is super easy and the tools are intuitive.
- ⚡ **Super fast** - It feels fast, and the actual experience is faster.

## Why 🙂??
Okay, I don't have to play subway-surface in the background while explaining this right? XD

You have a file on your computer that you want to share it with a bunch of people. But maybe this file have content that is againest your usual file sharing third-party service rules? Or maybe you just don't want to put such file in a service's cloud? Maybe this file exeeds the free size limit and the service wants you to pay to share now? IDC!

It's simple, FileMeQuietly will allow you to share your file directly with the people you want. No Censorship, No party in the middle and no size limit.

## Usage
You can either clone it and run it or download the latest compiled version of the app compatible with your system.

### Clone
To clone this project, run this on terminal:
```zsh
git clone https://github.com/SKbarbon/filemequietly.git
```
Then install the requirements in `requirements.txt` file. Make sure to create a new venv before that.

### Download
Currently in progress.

## Bruh, how the F does that work? XD
Will To achieve this "free-of-cost and no third-party involved in the middle" experience, I did follow this approach:

Your file is in your computer, the tool will start a local-host to host the file. But wait, how people on other network will access this host? We need someway to mirror a global URL to your locahost right?. So I used Ngrok APIs for this, and as you know it's totally free.

I am just a boy with an idea 👉👈🎀.