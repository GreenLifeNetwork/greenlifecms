const GreenLifeApp = () => {
    const md           = new MobileDetect(window.navigator.userAgent);
    const ios_url      = "https://apps.apple.com/us/app/green-lifestyle/id1484892517";
    const android_url  = "https://play.google.com/store/apps/details?id=lastchance.greenlife.quotes";
    const fallback_url = "https://greenlife.cloud/";
    let isDesktop = false;
    let isAndroid = false;
    let isIOS = false;
    if (md.os() == "iOS") {
        isIOS = true
    } else if (md.os() == "AndroidOS") {
        isAndroid = true
    } else {
        isDesktop = true
    }

    const overrideLinksWithAppStoreLink = () => {
        const articleLinks = document.querySelectorAll('article a')
        articleLinks.forEach(link => {
            link.href = isIOS ? ios_url : android_url
        })
    }


    if(isIOS || isAndroid) {
        overrideLinksWithAppStoreLink()
        if(isIOS) {
            document.querySelector('#ios-app-available').style.display = 'block'
        }
        if(isAndroid) {
            document.querySelector('#android-app-available').style.display = 'block'
        }
    }

}

GreenLifeApp()
