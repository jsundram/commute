// http://stackoverflow.com/questions/13944518/how-to-scrape-links-with-phantomjs
// http://docs.casperjs.org/en/latest/quickstart.html
var casper = require('casper').create();
var g_work_to_home = "https://www.google.com/maps/preview#!data=!1m4!1m3!1d181659!2d-122.3818491!3d37.6424559!4m27!3m18!1m2!1s1601+Willow+Rd%2C+Menlo+Park%2C+CA+94025!5e2!1m5!1s855+Folsom+St%2C+San+Francisco%2C+CA+94105!2s0x80858080bd6bcf2d%3A0xe0d6f48c3de86456!3m2!3d37.7810181!4d-122.4022291!3m8!1m3!1d245635!2d-122.244513!3d37.6422637!3m2!1i1676!2i933!4f13.1!5m2!13m1!1e1!7m4!11m3!1m1!1e1!2b1&fid=0";

var g_home_to_work = "https://www.google.com/maps/preview#!data=!4m31!3m22!1m5!1s855+Folsom+St%2C+San+Francisco%2C+CA+94105!2s0x80858080bd6bcf2d%3A0xe0d6f48c3de86456!3m2!3d37.7810181!4d-122.4022291!1m6!1s1601+Willow+Rd%2C+Menlo+Park%2C+CA+94025!2s0x808fbc97a45c99b1%3A0x2b4ba43d664b4206!3m2!3d37.4833782!4d-122.1495525!5e2!3m8!1m3!1d181659!2d-122.3818491!3d37.6424559!3m2!1i838!2i690!4f13.1!5m2!13m1!1e1!7m4!11m3!1m1!1e1!2b1&fid=0";

function getTime() {
    /*
        <div class="altroute-rcol altroute-aux"> 
            <img src="//maps.gstatic.com/mapfiles/transparent.png" class="dir-traffic dir-traffic-green"> 
            <span> In current traffic: 38 mins </span>  
        </div>
    */
    var sel = document.querySelectorAll('div.altroute-aux');
    return sel[0].innerText;
}

casper.start(g_work_to_home, function() {
    this.echo(this.getTitle());
    this.echo(this.evaluate(getTime));
});

casper.thenOpen(g_home_to_work, function() {
    this.echo(this.getTitle());
    this.echo(this.evaluate(getTime));
});

casper.run();
