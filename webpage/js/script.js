d3.select("#buttonCheck").on("click", function () {


    d3.select(".banner").select("img").remove();

    var inputValue = d3.select("#twitterHandleInput").property("value");

    if (inputValue) {
        d3.select(".message").text("Loading data...");
        var twitterName = '[{"name":"' + inputValue + '"}]';

        $.ajax({
            url: 'http://ec2-18-221-137-114.us-east-2.compute.amazonaws.com:80/result',
            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
            method: 'POST',
            dataType: 'json',
            data: twitterName,
            contentType: "application/json",
            success: function (response) {
                //console.log('success: ' + JSON.stringify(response));
                d3.select("#twitterHandleInput").property("value", "");
                d3.select(".message").text("");
                $('#myModal').modal('show');
                $('#myModal').on('shown.bs.modal', function (e) {
                    dataVizStuff(response);
                });
            },
            statusCode: {
                500: function () {
                    d3.select(".message").text("No Twitter profile found for " + inputValue + ".");
                    d3.select("#twitterHandleInput").property("value", "");
                }
            }
        })

    } else {
        d3.select("#twitterHandleInput").property("placeholder", "Please enter a Twitter handle")
    }

    //testing 

    // $('#myModal').modal('show');
    // $('#myModal').on('shown.bs.modal', function (e) {
    //     dataVizStuff();
    // });

});

function dataVizStuff(data) {

    // var data = {
    //     "twitter_data": {
    //         "avg_tweet_len": 124.52732919254659,
    //         "bot_or_not": 0,
    //         "bot_prob": 0.34455597400665283,
    //         "contributors_enabled": false,
    //         "created_at": "Wed Mar 18 13:46:38 +0000 2009",
    //         "default_profile": false,
    //         "default_profile_image": false,
    //         "description": "45th President of the United States of America🇺🇸",
    //         "error": "Profile",
    //         "favourites_count": 24,
    //         "follow_request_sent": false,
    //         "followers_count": 50680103,
    //         "following": false,
    //         "friends_count": 45,
    //         "geo_enabled": true,
    //         "id": 25073877,
    //         "is_translator": false,
    //         "label": 0,
    //         "lang": "en",
    //         "listed_count": 86490,
    //         "location": "Washington, DC",
    //         "name": "Donald J. Trump",
    //         "notifications": false,
    //         "num_retweet": 347,
    //         "political_profile": "Low",
    //         "political_score": 0,
    //         "profile_background_color": "6D5C18",
    //         "profile_background_image_url": "http://pbs.twimg.com/profile_background_images/530021613/trump_scotland__43_of_70_cc.jpg",
    //         "profile_background_image_url_https": "https://pbs.twimg.com/profile_background_images/530021613/trump_scotland__43_of_70_cc.jpg",
    //         "profile_background_tile": true,
    //         "profile_image_url": "https://twitter.com/realDonaldTrump/profile_image?size=original",
    //         "profile_image_url_https": "https://pbs.twimg.com/profile_images/874276197357596672/kUuht00m_normal.jpg",
    //         "profile_link_color": "1B95E0",
    //         "profile_sidebar_border_color": "BDDCAD",
    //         "profile_sidebar_fill_color": "C5CEC0",
    //         "profile_text_color": "333333",
    //         "profile_use_background_image": true,
    //         "protected": false,
    //         "screen_name": "realDonaldTrump",
    //         "statuses_count": 37299,
    //         "time_zone": "Eastern Time (US & Canada)",
    //         "ttl_tweet": 3220,
    //         "url": "https://t.co/OMxB0x7xC5",
    //         "utc_offset": -14400,
    //         "verified": true
    //     }
    // }



    //d3.json("data/mock_data_djt_v2.json", function (error, data) {
    //console.log(data.twitter_data.profile_banner_url)

    //(function() {    
    // .info
    d3.select(".banner").select("img").remove();

    d3.select(".banner")
        .append("img")
        .attr("src", data.twitter_data.profile_image_url)
        .attr("width", "100%");

    d3.select(".screen_name")
        .text(data.twitter_data.screen_name);

    d3.select(".name")
        .text(data.twitter_data.name);

    d3.select(".description")
        .text(data.twitter_data.description);

    d3.select(".location")
        .text(data.twitter_data.location);

    d3.select(".url")
        .html("<a href=" + data.twitter_data.url + " target=_blank>" + data.twitter_data.url + "</a>");

    d3.select(".created_at")
        .text(data.twitter_data.created_at);

    // d3.select(".most_recent_post")
    //     .text(data.twitter_data.created_at);

    d3.select(".id")
        .text(data.twitter_data.id);

    d3.select(".lang")
        .text(data.twitter_data.lang);

    d3.select(".time_zone")
        .text(data.twitter_data.time_zone);

    d3.select(".ttl_tweet")
        .text(data.twitter_data.ttl_tweet)

    d3.select(".avg_tweet_len")
        .text(data.twitter_data.avg_tweet_len)


    // .data-vis
    // var botValue = +data.bot_profile.score;
    // var politicalPropagandaValue = +data.political_profile.score;


    d3.select(".is-bot")
        .classed("red", data.twitter_data.bot_or_not === 1)
        .classed("green", data.twitter_data.bot_or_not === 0)
        .html(function () {
            return data.twitter_data.bot_or_not === 1
                ? "YES"
                : "NO"
        })


    d3.select(".friends")
        .text(data.twitter_data.friends_count);

    d3.select(".followers")
        .text(data.twitter_data.followers_count);

    d3.select(".verified")
        .text(data.twitter_data.verified);

    d3.select(".default-profile")
        .text(data.twitter_data.default_profile);

    var common_topic = [
        [
            data.twitter_data.word1,
            +data.twitter_data.word1_count
        ],
        [
            data.twitter_data.word2,
            +data.twitter_data.word2_count
        ],
        [
            data.twitter_data.word3,
            +data.twitter_data.word3_count
        ],
        [
            data.twitter_data.word4,
            +data.twitter_data.word4_count
        ],
        [
            data.twitter_data.word5,
            +data.twitter_data.word5_count
        ]
    ];

    var recentTweets = [
        data.twitter_data.tweets1,
        data.twitter_data.tweets2,
        data.twitter_data.tweets3,
        data.twitter_data.tweets4,
        data.twitter_data.tweets5,
    ]

    var botWidth = parseInt(d3.select(".bot").style("width"));

    d3.select(window).on("resize", resize);

    // d3.select(".political-propaganda-inner")
    //     .text(data.twitter_data.political_score.toUpperCase());

    // if (data.twitter_data.political_score === "High") {
    //     d3.select(".political-propaganda-inner")
    //     .style("height", botWidth * 2 / 3)    
    //     .style("color", "red")
    // }   
    // if (data.twitter_data.political_score === "Medium") {
    //     d3.select(".political-propaganda-inner")
    //     .style("height", botWidth * 2 / 3)  
    //     .style("color", "yellow")
    // }
    // if (data.twitter_data.political_score === "Low") {
    //     d3.select(".political-propaganda-inner")
    //     .style("height", botWidth * 2 / 3)  
    //     .style("color", "green")
    // }  


    function resize() {
        botWidth = parseInt(d3.select(".bot").style("width")) - 30;
        //var commonTopicsWidth = parseInt(d3.select(".common-topics-from-tweets").style("width"));
        circle(".bot", botWidth, Math.round(data.twitter_data.bot_prob * 100));
        label(".political-propaganda", botWidth, data.twitter_data.political_profile);
        // circle(".political-propaganda", botWidth, politicalPropagandaValue * 100);
        // barsFeatures(".profile-features", botWidth, data.bot_profile);
        // barsFeatures(".languge-features", botWidth, data.political_profile);
        commonTopics(".common-topics-from-tweets", botWidth, common_topic);
        recentTweetsFunc(".recent-tweets", recentTweets);
    }

    resize();

    function recentTweetsFunc(element, data) {

        d3.select(element + " > table").remove();
        var table = d3.select(element).append("table")
            .attr("class", "table table-sm table-features")
            .selectAll("tr").data(data);

        var tr = table.enter().append("tr");


        tr.append("td").append("text")
            .text(function (d, i) { return (i + 1) + "."; })
        tr.append("td")
            .append("text").text(function (d) {
                return d;
            })
    };

    //}())

    function label(element, width, data) {

        d3.select(element + " > svg").remove();

        var width = width,
            height = width * 2 / 3,
            radius = (height / 2) - (height / 15),
            arcWidth = radius / 4;

        var svg = d3.select(element).append("svg")
            .attr("width", width)
            .attr("height", height);

        var g = svg.append("g").attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");


        var fill;

        if (data === "High") {
            fill = "red";
        }
        if (data === "Medium") {
            fill = "yellow";
        }
        if (data === "Low") {
            fill = "green";
        }

        g.append("text")
            .attr("text-anchor", "middle")
            .attr("dominant-baseline", "central")
            .attr("fill", fill)
            .attr("font-weight", "bold")
            .attr('font-size', height / 4)
            .text(data.toUpperCase());

    }



    function circle(element, width, data) {

        d3.select(element + " > svg").remove();

        var width = width,
            height = width * 2 / 3,
            radius = (height / 2) - (height / 15),
            arcWidth = radius / 4;

        var tau = 2 * Math.PI;

        var arc = d3.arc()
            .outerRadius(radius)
            .innerRadius(radius - arcWidth)
            .startAngle(0);

        var svg = d3.select(element).append("svg")
            .attr("width", width)
            .attr("height", height);

        var g = svg.append("g").attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

        var background = g.append("path")
            .datum({ endAngle: tau })
            .style("fill", "steelblue")
            .attr("d", arc);

        var foreground = g.append("path")
            .datum({ endAngle: 0.01 * tau })
            .style("fill", "darkred")
            .attr("d", arc);

        g.append("text")
            .attr("text-anchor", "middle")
            .attr("dominant-baseline", "central")
            .attr("fill", "darkred")
            .attr("font-weight", "bold")
            .attr('font-size', height / 4)
            .text(data + " %");

        foreground.transition()
            .duration(750)
            .attrTween("d", arcTween((data / 100) * tau));

        function arcTween(newAngle) {
            return function (d) {
                var interpolate = d3.interpolate(d.endAngle, newAngle);
                return function (t) {
                    d.endAngle = interpolate(t);
                    return arc(d);
                };
            };
        }



    }

    function barsFeatures(element, width, data0) {

        d3.select(element + " > svg").remove();

        var widthSvg = width,
            heightSvg = width * 2 / 3
        margin = { top: 0, right: 20, bottom: 10, left: 0 },
            height = width * 2 / 3 - margin.top - margin.bottom,
            width = width - margin.left - margin.right;

        var svg = d3.select(element).append("svg")
            .attr("width", widthSvg)
            .attr("height", heightSvg);



        var dataArr = [];

        for (d in data0) {
            var tempArr = {};
            tempArr.name = (d[0].toUpperCase() + d.slice(1)).split("_").join(" ");
            tempArr.value = +data0[d];
            dataArr.push(tempArr)
        }

        var data = dataArr.slice(1);

        var yScale = d3.scaleBand().rangeRound([0, height]).padding(0.45)
            .domain(data.map(function (d) {
                return d.name;
            })),
            xScale = d3.scaleLinear().rangeRound([0, width])
                .domain([0, 1]);

        var group = svg.append("g")
            .attr("transform", "translate(" + [margin.left, margin.top] + ")");

        var bars = group
            .selectAll("rect")
            .data(data);

        var labels = group
            .selectAll("text")
            .data(data);

        bars
            .enter()
            .append("rect")
            .attr("class", "bar")
            .attr("width", function (d, i) {
                return 0;
            })
            .attr("height", yScale.bandwidth())
            .attr("x", 0)
            .attr("y", function (d, i) {
                return yScale(d.name);
            })
            .style("fill", "steelblue")
            .transition()
            .duration(750)
            .attr("width", function (d, i) {
                return xScale(d.value);
            })


        labels
            .enter()
            .append("text")
            .attr("class", "label")

            .attr("x", 0)
            .attr("y", function (d, i) {
                return yScale(d.name) - 2;
            })
            .text(function (d, i) {
                return d.name; //  + " " + d.value * 100 + "%"
            })
            .style("font-size", 11)

        labels
            .enter()
            .append("text")
            .style("opacity", 0)
            .attr("class", "label")

            .attr("x", function (d, i) {
                return d.value < 0.15
                    ?
                    xScale(d.value) + 2
                    :
                    xScale(d.value) - 4;
            })
            .attr("y", function (d, i) {
                return yScale(d.name) + yScale.bandwidth() / 2;
            })
            .attr("text-anchor", function (d, i) {
                return d.value < 0.15
                    ?
                    "start"
                    :
                    "end";
            })
            .attr("dominant-baseline", "central")
            .text(function (d, i) {
                return d.value * 100 + "%";
            })
            .style("font-size", 13)
            .style("font-weight", "bold")
            .style("fill", function (d, i) {
                return d.value < 0.15
                    ?
                    "steelblue"
                    :
                    "white";
            })
            .transition()
            .duration(750)
            .style("opacity", 1);

    }

    function commonTopics(element, width, data0) {

        d3.select(element + " > svg").remove();

        var widthSvg = width,
            heightSvg = width / 3
        margin = { top: 0, right: 30, bottom: 0, left: width / 4 },
            height = (width / 3) - margin.top - margin.bottom,
            width = width - margin.left - margin.right;

        var svg = d3.select(element).append("svg")
            .attr("width", widthSvg)
            .attr("height", heightSvg);



        var data = [];

        data0.forEach(function (d) {
            data.push({ name: d[0], value: d[1] });
        })




        var yScale = d3.scaleBand().rangeRound([0, height]).padding(0.2)
            .domain(data.map(function (d) {
                return d.name;
            })),
            xScale = d3.scaleLinear().rangeRound([0, width])
                .domain([0, d3.max(data, function (d) {
                    return d.value;
                })]);


        var group = svg.append("g")
            .attr("transform", "translate(" + [margin.left, margin.top] + ")");

        var bars = group
            .selectAll("rect")
            .data(data);

        var labels = group
            .selectAll("text")
            .data(data);

        bars
            .enter()
            .append("rect")
            .attr("class", "bar")
            .attr("width", function (d, i) {
                return 0;
            })
            .attr("height", yScale.bandwidth())
            .attr("x", 0)
            .attr("y", function (d, i) {
                return yScale(d.name);
            })
            .style("fill", "steelblue")
            .transition()
            .duration(750)
            .attr("width", function (d, i) {
                return xScale(d.value);
            })

        labels
            .enter()
            .append("text")
            .attr("class", "label")

            .attr("x", -5)
            .attr("y", function (d, i) {
                return yScale(d.name) + yScale.bandwidth() / 2;
            })
            .attr("text-anchor", function (d, i) {
                return "end";
            })
            .attr("dominant-baseline", "central")
            .text(function (d, i) {
                return d.name;
            })
            .style("font-size", 13)
            .style("font-weight", "bold")
            .style("fill", function (d, i) {
                return "steelblue";
            });

        labels
            .enter()
            .append("text")
            .attr("class", "label")

            .attr("x", function (d, i) {
                return xScale(d.value) - 5;
            })
            .attr("y", function (d, i) {
                return yScale(d.name) + yScale.bandwidth() / 2;
            })
            .attr("text-anchor", function (d, i) {
                return "end";
            })
            .attr("dominant-baseline", "central")
            .text(function (d, i) {
                return d.value;
            })
            .style("font-size", 13)
            .style("font-weight", "bold")
            .style("fill", function (d, i) {
                return "white";
            });
    }
}