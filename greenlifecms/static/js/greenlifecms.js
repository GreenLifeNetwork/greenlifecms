const isNativeApp = window.isNativeApp || location.search.indexOf("isNativeApp") > -1
const GreenLifeApp = () => {
  const md = new MobileDetect(window.navigator.userAgent)
  let isDesktop = false
  let isAndroid = false
  let isIOS = false
  if (md.os() === "iOS") {
    isIOS = true
  } else if (md.os() === "AndroidOS") {
    isAndroid = true
  } else {
    isDesktop = true
  }
  if (isIOS || isAndroid) {
    if (isIOS) {
      document.querySelector("#ios-app-available").style.display = "block"
    }
    if (isAndroid) {
      document.querySelector("#android-app-available").style.display = "block"
    }
    document.querySelector('.content').style.display = "none"
  }
}

if (!isNativeApp) {
  GreenLifeApp()
} else {
  window.addEventListener("DOMContentLoaded", (event) => {
    document.querySelector("footer").style.display = "none"
  })
}
