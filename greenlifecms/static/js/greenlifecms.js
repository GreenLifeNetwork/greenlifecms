const isNativeApp = window.isNativeApp || location.search.indexOf("isNativeApp") > -1

function addScript(href) {
    var s = document.createElement('script');
    s.type = 'text/javascript';
    s.src = href;
    document.getElementsByTagName('head')[0].appendChild(s);
    console.log('add script', href)
}

const GreenLifeApp = () => {
  const md = new MobileDetect(window.navigator.userAgent)
  const isNudgePage = location.href.indexOf('/g/') > -1
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
  console.log('isIOS', isIOS)
  console.log('isAndroid', isAndroid)
  console.log('isDesktop', isDesktop)
  if (isIOS || isAndroid) {
    document.querySelector("#app-available").style.display = "block"
    if (isIOS) {
      document.querySelector("#ios-app-available").style.display = "block"
      document.querySelector("#android-app-available").style.display = "none"
    }
    if (isAndroid) {
      document.querySelector("#android-app-available").style.display = "block"
      document.querySelector("#ios-app-available").style.display = "none"
    }
    document.querySelector('.content').style.display = "none"
  } else if (isDesktop) {
    if (document.querySelector("#app-available-desktop-banner")) {
        document.querySelector("#app-available-desktop-banner").style.display = "block"
    }
    addScript("https://platform-api.sharethis.com/js/sharethis.js#property=5fc2db2431564700129f78e8")
  }

    (function(b,r,a,n,c,h,_,s,d,k){if(!b[n]||!b[n]._q){for(;s<_.length;)c(h,_[s++]);d=r.createElement(a);d.async=1;d.src="https://cdn.branch.io/branch-latest.min.js";k=r.getElementsByTagName(a)[0];k.parentNode.insertBefore(d,k);b[n]=h}})(window,document,"script","branch",function(b,r){b[r]=function(){b._q.push([r,arguments])}},{_q:[],_v:1},"addListener applyCode autoAppIndex banner closeBanner closeJourney creditHistory credits data deepview deepviewCta first getCode init link logout redeem referrals removeListener sendSMS setBranchViewData setIdentity track validateCode trackCommerceEvent logEvent disableTracking".split(" "), 0);

  console.log('branch', branch)
    branch.init('key_live_dhJ1Y7Xg8VsRsfLNzrRo7loayFgKElc6');
}

if (!isNativeApp) {
  GreenLifeApp()
} else {
  window.addEventListener("DOMContentLoaded", (event) => {
    document.querySelector("footer").style.display = "none"
    document.querySelector(".app-banner").style.display = "none"
    document.querySelector(".sharethis-inline-share-buttons").style.display = "none"
    if(document.querySelector(".app-banner-intro")) {
        document.querySelector(".app-banner-intro").style.display = "none"
    }
  })
}

// https://codepen.io/l422y/pen/cdwhm
var ringer = {
  //countdown_to: "10/31/2014",
  countdown_to: "01/01/2028",
  rings: {
    'YEARS': {
      s: 86400000 * 365, // mseconds in a day,
      max: 100
    },
    'MONTHS': {
      s: (86400000 * 365) / 12, // mseconds in a day,
      max: 12
    },
//    'DAYS': {
//      s: 86400000, // mseconds in a day,
//      max: 365
//    },
    'HOURS': {
      s: 3600000, // mseconds per hour,
      max: 24
    },
    'MINUTES': {
      s: 60000, // mseconds per minute
      max: 60
    },
    'SECONDS': {
      s: 1000,
      max: 60
    },
    'MICROSEC': {
      s: 10,
      max: 100
    }
   },
  r_count: 5,
  r_spacing: 10, // px
  r_size: 100, // px
  r_thickness: 5, // px
  update_interval: 11, // ms


  init: function(){

    $r = ringer;
    $r.cvs = document.createElement('canvas');

    $r.size = {
      w: ($r.r_size + $r.r_thickness) * $r.r_count + ($r.r_spacing*($r.r_count-1)),
      h: ($r.r_size + $r.r_thickness)
    };


    $r.cvs.setAttribute('width',$r.size.w);
    $r.cvs.setAttribute('height',$r.size.h);
    $r.ctx = $r.cvs.getContext('2d');
    $(".countdown").append($r.cvs);
    $r.cvs = $($r.cvs);
    $r.ctx.textAlign = 'center';
    $r.actual_size = $r.r_size + $r.r_thickness;
    $r.countdown_to_time = new Date($r.countdown_to).getTime();
    $r.cvs.css({ width: $r.size.w+"px", height: $r.size.h+"px" });
    if (document.querySelector('.countdown-container canvas')) {
        document.querySelector('.countdown-container canvas').style.width = 'auto'
        document.querySelector('.countdown-container canvas').style.height = '50px'
    }
    $r.go();
  },
  ctx: null,
  go: function(){
    var idx=0;

    $r.time = (new Date().getTime()) - $r.countdown_to_time;


    for(var r_key in $r.rings) $r.unit(idx++,r_key,$r.rings[r_key]);

    setTimeout($r.go,$r.update_interval);
  },
  unit: function(idx,label,ring) {
    var x,y, value, ring_secs = ring.s;
    value = parseFloat($r.time/ring_secs);
    $r.time-=Math.round(parseInt(value)) * ring_secs;
    value = Math.abs(value);

    x = ($r.r_size*.5 + $r.r_thickness*.5);
    x +=+(idx*($r.r_size+$r.r_spacing+$r.r_thickness));
    y = $r.r_size*.5;
    y += $r.r_thickness*.5;


    // calculate arc end angle
    var degrees = 360-(value / ring.max) * 360.0;
    var endAngle = degrees * (Math.PI / 180);

    $r.ctx.save();

    $r.ctx.translate(x,y);
    $r.ctx.clearRect($r.actual_size*-0.5,$r.actual_size*-0.5,$r.actual_size,$r.actual_size);

    // first circle
    $r.ctx.strokeStyle = "rgba(128,128,128,0.2)";
    $r.ctx.beginPath();
    $r.ctx.arc(0,0,$r.r_size/2,0,2 * Math.PI, 2);
    $r.ctx.lineWidth =$r.r_thickness;
    $r.ctx.stroke();

    // second circle
    $r.ctx.strokeStyle = "rgba(24, 190, 0, 0.9)";
    $r.ctx.beginPath();
    $r.ctx.arc(0,0,$r.r_size/2,0,endAngle, 1);
    $r.ctx.lineWidth =$r.r_thickness;
    $r.ctx.stroke();

    // label
    $r.ctx.fillStyle = "#ffffff";

    $r.ctx.font = '12px Helvetica';
    $r.ctx.fillText(label, 0, 23);
    $r.ctx.fillText(label, 0, 23);

    $r.ctx.font = 'bold 40px Helvetica';
    $r.ctx.fillText(Math.floor(value), 0, 10);

    $r.ctx.restore();
  }
}

if(location.search === "") {
ringer.init();
}
