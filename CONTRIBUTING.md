# Contributing

## Basic Flow of Contributing Code
If you are already familiar with Git/GitHub and contributing to Open Source projects, the basic flow of contribution is as follows:

1. Fork the repo
2. Clone your forked repo
3. Checkout a feature branch or the `dev` branch depending on the scope of the changes
4. Make commits and push changes to your forked repo
5. Make a Pull Request that clearly describes your changes and the reason for your changes with `dev` as the base and your fork/branch as the head/compare
6. Allow some time for others to review/make comments on your code. Post on an appropriate Slack channel/tag appropriate users as you see fit; PR's should generally not be merged without review.

If you are less familiar with Git/GitHub and need more detail on how exactly this process works, keep reading.

## Contributing In Detail

This will assume you are using the command-line version of git. 

* First, fork the main repo into your own account on GitHub. Do this by clicking the "Fork" button on the top right of the [home page](https://github.com/ASU-CodeDevils/Cryptopotamus) of the repo.
* Next, clone the repo to a local version. You can do this by executing this command:

```sh
git clone https://github.com/<your username>/cryptopotamus
```

* You now have two "personal" versions of the repo. One that is hosted on github under your GitHub account, which you can access at the url https://github.com/your_username/cryptopotamus, and one on your local computer. Finally, there is the main repo which will always be accessed at https://github.com/asu-codedevils/cryptopotamus. By cloning your forked repository, git automatically set up a remote named `origin` for you, which links to your forked version. It's also often handy to set up a remote with the main repository's URL. You can do this by executing:

```sh
git remote add upstream https://github.com/asu-codedevils/cryptopotamus
```

This will add a remote to your local repository with the name `upstream` which links to the main shared repository.

* Now you should check out the `dev` branch by doing

```sh
git checkout dev
```

* Depending on the nature of your changes, you may also want to make a new feature branch based on the develop branch. To do this, *while you have develop checked out*, execute:

```sh
git checkout -b <new branch name>
```

This will create a new branch with the specified name.

* At this point, you should make your changes, then stage and commit them as normal. Try to make your commit messages meaningful.

* When your changes are ready, you'll want to push them up to your forked repository. To do this, make sure your changes are all committed, then do

```sh
git push
```

* If you are working on a newly-created feature branch, git may complain to you saying that you need to set an upstream url for the new branch. To do this, run the command

```sh
git push -u origin <current branch name>
```

(or the longhand version:)

```sh
git push --set-upstream origin <current branch name>
```

This will set the current local branch to track the remote repo origin (your forked version of the repo on your github account) on the branch `<current branch name>`, and then push your changes to that branch.

* Now open github to the forked repo on your account. You should be able to select the correct branch from the branch drop-down menu in the center-left of the screen and then see your changes reflected. Now it's time to make Pull Request on the main repo.

* Open up the [main repo](https://github.com/asu-codedevils/cryptopotamus) and click on the "Pull Requests" tab near the top of the screen. Click on "New pull request" and then click the link that says "compare across forks". On the left side just below that, you should have `base fork: ASU-CodeDevils/Cryptopotamus` `base: master` and on the right you should click on the dropdowns and select your fork (labelled `<your username>/cryptopotamus`) and then the correct branch that you made modifications to.

* Now make a title and for your PR and describe the changes you made, then create the PR. Yay! Now just wait for feedback/review and hopefully your changes will be merged.

## Rebasing Changes

*This section not written yet, but planned for the future*

# Code of Conduct
## Conduct
We are committed to providing a friendly, safe and welcoming environment for all, regardless of level of experience, gender identity and expression, sexual orientation, disability, personal appearance, body size, race, ethnicity, age, religion, nationality, or other similar characteristic.

* On Slack, please avoid using overtly sexual nicknames or other nicknames that might detract from a friendly, safe and welcoming environment for all.
* Please be kind and courteous. There’s no need to be mean or rude.
* Respect that people have differences of opinion and that every design or implementation choice carries a trade-off and numerous costs. There is seldom a right answer.
* Please keep unstructured critique to a minimum. If you have solid ideas you want to experiment with, make a fork and see how it works.
* We will exclude you from interaction if you insult, demean or harass anyone. That is not welcome behaviour. We interpret the term “harassment” as including the definition in the Citizen Code of Conduct; if you have any lack of clarity about what might be included in that concept, please read their definition. In particular, we don’t tolerate behavior that excludes people in socially marginalized groups.
* Private harassment is also unacceptable. No matter who you are, if you feel you have been or are being harassed or made uncomfortable by a community member, please contact one of the channel ops or any of the Rust moderation team immediately. Whether you’re a regular contributor or a newcomer, we care about making this community a safe place for you and we’ve got your back.
* Likewise any spamming, trolling, flaming, baiting or other attention-stealing behaviour is not welcome.

## Moderation
These are the policies for upholding our community’s standards of conduct. If you feel that a thread needs moderation, please contact the project leads and/or CodeDevils staff.

* Remarks that violate the Rust standards of conduct, including hateful, hurtful, oppressive, or exclusionary remarks, are not allowed. (Cursing is allowed, but never targeting another user, and never in a hateful manner.)
* Remarks that moderators find inappropriate, whether listed in the code of conduct or not, are also not allowed.
* Moderators will first respond to such remarks with a warning.
* If the warning is unheeded, the user will be “kicked,” i.e., kicked out of the communication channel to cool off.
* If the user comes back and continues to make trouble, they will be banned, i.e., indefinitely excluded.
* Moderators may choose at their discretion to un-ban the user if it was a first offense and they offer the offended party a genuine apology which is accepted, and if the banned user demonstrates a concerted effort or intent not to continue the same behavior in the future.
* If a moderator bans someone and you think it was unjustified, please take it up with that moderator, or with a different moderator, in private. Complaints about bans in-channel are not allowed.
* Moderators are held to a higher standard than other community members. If a moderator creates an inappropriate situation, they should expect less leeway than others.

In the CodeDevils community we strive to go the extra step to look out for each other. Don’t just aim to be technically unimpeachable, try to be your best self. In particular, avoid flirting with offensive or sensitive issues, particularly if they’re off-topic; this all too often leads to unnecessary fights, hurt feelings, and damaged trust; worse, it can drive people away from the community entirely.

And if someone takes issue with something you said or did, resist the urge to be defensive. Just stop doing what it was they complained about and apologize. Even if you feel you were misinterpreted or unfairly accused, chances are good there was something you could’ve communicated better — remember that it’s your responsibility to make your fellow CodeDevils comfortable. Everyone wants to get along and we are all here first and foremost because we want to talk about cool technology. You will find that people will be eager to assume good intent and forgive as long as you earn their trust.

*Adapted from the [Rust Code of Conduct]() which is in turn adapted from the [Node.js Policy on Trolling](http://blog.izs.me/post/30036893703/policy-on-trolling) as well as the [Contributor Covenant v1.3.0.](https://www.contributor-covenant.org/version/1/3/0/code-of-conduct.html)*