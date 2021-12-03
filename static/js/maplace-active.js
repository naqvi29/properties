$(function() {
               
            var LocsA = [
                {
                    lat: 40.740178,
                    lon: -74.190194,
                    title: 'Property 1',
                    html: ['<a href="single-properties.html"><img style="width: 250px;" alt="" src="img/property/7.jpg"></a>',
                           '<h6 style="margin: 15px 0 5px;color: #004395;"><a href="single-properties.html">Friuli-Venezia Giulia</a></h6>',
                            '<h5 style="margin: 0;color: #f9c322;" class="price">$52,354</h5>',
                            '<p style="margin: 0;font-weight: 300;">568 E 1st Ave, Miami</p>'
                        ].join(''),
                    icon: 'img/map-marker-2.png',
                },
                {
                    lat: 40.733617,
                    lon: -74.171150,
                    title: 'Property 2',
                    html: ['<a href="single-properties.html"><img style="width: 250px;" alt="" src="img/property/3.jpg"></a>',
                           '<h6 style="margin: 15px 0 5px;color: #004395;"><a href="single-properties.html">Radison de Villa</a></h6>',
                            '<h5 style="margin: 0;color: #f9c322;" class="price">$42,354</h5>',
                            '<p style="margin: 0;font-weight: 300;"> 450 E 1st Ave, New Jersey</p>'
                        ].join(''),
                    icon: 'img/map-marker-2.png',
                    animation: google.maps.Animation.BOUNCE
                },
                {
                    lat: 40.743011,
                    lon: -74.247100,
                    title: 'Property 3',
                    html: ['<a href="single-properties.html"><img style="width: 250px;" alt="" src="img/property/4.jpg"></a>',
                           '<h6 style="margin: 15px 0 5px;color: #004395;"><a href="single-properties.html">Friuli-Venezia Giulia</a></h6>',
                            '<h5 style="margin: 0;color: #f9c322;" class="price">$62,354</h5>',
                            '<p style="margin: 0;font-weight: 300;">568 E 2nd Ave, Miami</p>'
                        ].join(''),
                    icon: 'img/map-marker-2.png',
                    animation: google.maps.Animation.BOUNCE
                },
                {
                    lat: 40.711150,
                    lon: -74.214998,
                    title: 'Property 4',
                    html: ['<a href="single-properties.html"><img style="width: 250px;" alt="" src="img/property/5.jpg"></a>',
                           '<h6 style="margin: 15px 0 5px;color: #004395;"><a href="single-properties.html">Friuli-Venezia Giulia</a></h6>',
                            '<h5 style="margin: 0;color: #f9c322;" class="price">$22,354</h5>',
                            '<p style="margin: 0;font-weight: 300;">568 E 1st Ave, Miami</p>'
                        ].join(''),
                    icon: 'img/map-marker-2.png',
                    animation: google.maps.Animation.BOUNCE
                },
                {
                    lat: 40.690010,
                    lon: -74.151753,
                    title: 'Property 5',
                    html: ['<a href="single-properties.html"><img style="width: 250px;" alt="" src="img/property/6.jpg"></a>',
                           '<h6 style="margin: 15px 0 5px;color: #004395;"><a href="single-properties.html">Friuli-Venezia Giulia</a></h6>',
                            '<h5 style="margin: 0;color: #f9c322;" class="price">$62,354</h5>',
                            '<p style="margin: 0;font-weight: 300;">568 E 1st Ave, Miami</p>'
                        ].join(''),
                    icon: 'img/map-marker-2.png',
                    animation: google.maps.Animation.BOUNCE
                },
                {
                    lat: 40.697590,
                    lon: -74.263164,
                    title: 'Property 6',
                    html: ['<a href="single-properties.html"><img style="width: 250px;" alt="" src="img/property/8.jpg"></a>',
                           '<h6 style="margin: 15px 0 5px;color: #004395;"><a href="single-properties.html">Marvel de Villa</a></h6>',
                            '<h5 style="margin: 0;color: #f9c322;" class="price">$42,354</h5>',
                            '<p style="margin: 0;font-weight: 300;">568 E 1st Ave, Miami</p>'
                        ].join(''),
                    icon: 'img/map-marker-2.png',
                    animation: google.maps.Animation.BOUNCE
                },
                {
                    lat: 40.729979,
                    lon: -74.271992,
                    title: 'Property 7',
                    html: ['<a href="single-properties.html"><img style="width: 250px;" alt="" src="img/property/10.jpg"></a>',
                           '<h6 style="margin: 15px 0 5px;color: #004395;"><a href="single-properties.html">Friuli-Venezia Giulia</a></h6>',
                            '<h5 style="margin: 0;color: #f9c322;" class="price">$34,354</h5>',
                            '<p style="margin: 0;font-weight: 300;">568 E 1st Ave, Miami</p>'
                        ].join(''),
                    icon: 'img/map-marker-2.png',
                    animation: google.maps.Animation.BOUNCE
                },
                {
                    lat: 40.727660,
                    lon: -74.156292,
                    title: 'property 7',
                    html: ['<a href="single-properties.html"><img style="width: 250px;" alt="" src="img/property/11.jpg"></a>',
                           '<h6 style="margin: 15px 0 5px;color: #004395;"><a href="single-properties.html">Friuli-Venezia Giulia</a></h6>',
                            '<h5 style="margin: 0;color: #f9c322;" class="price">$42,354</h5>',
                            '<p style="margin: 0;font-weight: 300;">568 E 1st Ave, Miami</p>'
                        ].join(''),
                    icon: 'img/map-marker-2.png',
                    animation: google.maps.Animation.BOUNCE
                },
                {
                    lat: 40.749702,
                    lon: -74.163631,
                    title: 'Property 8',
                    html: ['<a href="single-properties.html"><img style="width: 250px;" alt="" src="img/property/12.jpg"></a>',
                           '<h6 style="margin: 15px 0 5px;color: #004395;"><a href="single-properties.html">Friuli-Venezia Giulia</a></h6>',
                            '<h5 style="margin: 0;color: #f9c322;" class="price">$42,354</h5>',
                            '<p style="margin: 0;font-weight: 300;">568 E 1st Ave, Miami</p>'
                        ].join(''),
                    icon: 'img/map-marker-2.png',
                    animation: google.maps.Animation.BOUNCE
                },
                {
                    lat: 40.718971,
                    lon: -74.323219,
                    title: 'Property 9',
                    html: ['<a href="single-properties.html"><img style="width: 250px;" alt="" src="img/property/13.jpg"></a>',
                           '<h6 style="margin: 15px 0 5px;color: #004395;"><a href="single-properties.html">Friuli-Venezia Giulia</a></h6>',
                            '<h5 style="margin: 0;color: #f9c322;" class="price">$42,354</h5>',
                            '<p style="margin: 0;font-weight: 300;">568 E 1st Ave, Miami</p>'
                        ].join(''),
                    icon: 'img/map-marker-2.png',
                    animation: google.maps.Animation.BOUNCE
                },
                {
                    lat: 40.748350,
                    lon: -74.323219,
                    title: 'Property 10',
                    html: ['<a href="single-properties.html"><img style="width: 250px;" alt="" src="img/property/5.jpg"></a>',
                           '<h6 style="margin: 15px 0 5px;color: #004395;"><a href="single-properties.html">Friuli-Venezia Giulia</a></h6>',
                            '<h5 style="margin: 0;color: #f9c322;" class="price">$42,354</h5>',
                            '<p style="margin: 0;font-weight: 300;">568 E 1st Ave, Miami</p>'
                        ].join(''),
                    icon: 'img/map-marker-2.png',
                    animation: google.maps.Animation.BOUNCE
                }
            
                
            ];
            new Maplace({
                locations: LocsA,
                controls_on_map: true,
                map_options: {
                    zoom: 13,
                    scrollwheel: false,
                    stopover: true
                }
            }).Load();

        });