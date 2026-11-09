# Get started via Shopify CLI

How to quickly get started with the project

## Prerequisites

-   Have [Shopify CLI](https://shopify.dev/themes/tools/cli/installation) installed
-   Have [NPM](https://nodejs.org/en/download/) installed (any version above 10)
-   Have [Yarn](https://classic.yarnpkg.com/lang/en/docs/install/#mac-stable) installed (optional)

## .env

This file should contain the `.myshopify.com` URL for the project. This is required.

It's also a hidden file, so you might need to adjust the preferences of your editor or file explorer to see it in some cases.

## Install dependencies

Run `yarn` or `npm i` to install all the packages.

## Logging into Shopify CLI

Shopify CLI keeps you logged into a profile, so if you have worked on a different project that you utilized the CLI or this is the first time using the CLI, run the command below.

Run `yarn login:shopify` or `npm run login:shopify` and login to an account with access to the site you're working with

## Download theme from Shopify store

This should only be run on the init of the repo. Please do not run this on an existing repo, as it should not be required.

Run `yarn dl:theme` or `npm run dl:theme` and select the theme you would like to download. It's recommended to download the live theme.

## Serve Shopify store locally

It will serve your Shopify store locally, and it will output three links for you to use:

-   Localhost URL for the theme
-   Link to the online editor for the theme being worked on
    -   **Theme customizer changes will not be stored in the theme's code using this URL and will need to be remade once you publish the changes - it's recommended to have a dev theme connected to a Github dev branch and making the edits on that dev theme's customizer to retain the modifications**
-   A preview link that can be shared with anyone

Run `yarn dev` or `npm run dev` to serve the Shopify theme locally.

## Delete all unstaged changes

It will delete all changes that have not been staged or committed to the repo to restart where you began.

Run `yarn clean` or `npm run clean` to delete all unstaged changes.
