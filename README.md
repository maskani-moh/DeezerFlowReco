# Data Science Game 2017 Challenge

This project was started in the context of the international competition of the **Data Science Game** organized each year and gathering more than 120 teams from all around the World !

Collaborators on this project are:
* Joseph Enguehard
* Anthony Hu
* Nicolas Cherel
* Maskani Filali Mohamed

----
### Description

Getting the perfect music recommendation is a challenging task. Who has never dreamt of laying back and listening to some music, while having no buttons to press at all and still getting the perfect tune? But what defines this perfect tune?

**Deezer** is a music streaming app, also available on the web. It proposes more than 43 million tracks and is available in more than 180 countries, through a free limited service and a premium offer.

For this online challenge, *Deezer* wants you to look at ***Flow***, its own music recommendation radio. The concept of *Flow* is simple: it uses collaborative filtering to provide a user with the music he wants to listen at the time he wants.... And if he does not want to listen to some specific tracks and skips songs by pressing the 'Next song' button, then the algorithm should detect it quickly. **In this context, getting the first song recommendation right is really important.**

### Goal

The goal of this challenge is to **predict whether the users of the test dataset listened to the first track Flow proposed them or not**. Deezer considers that a track is **listened** if the user has listened to **more than 30 seconds** of it `is_listened =1`. If the user presses the skip button to change the song **before 30 seconds**, then the track is not considered as being listened `is_listened = 0`.

The test dataset consists in a list of the first recommended tracks on *Flow* for several users. **Each row represents one user.**

The train dataset was generated using the listening history of these *Deezer* users for **one month**. Each row represents one listened track. **The list of distinct users in the train dataset matches exactly with the test dataset's one.**

