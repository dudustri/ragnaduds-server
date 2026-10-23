// RagnaDuds: roBrowser settings, the same on your PC (http://127.0.0.1:3338/) and on the site (/play/).
// Every URL is built from the page's own address, so the GRF files and the game proxy are always this server.
(function () {
	var base = location.origin + location.pathname.replace(/[^/]*$/, ''); // ".../" or ".../play/"
	window.ROConfigLocal = {
		servers: [{
			display: 'RagnaDuds Pre-Renewal',
			desc: 'Pre-Renewal · classic 99/70',
			address: 'host.docker.internal', // the game servers, as the proxy container sees them
			port: 6900,
			langtype: 0,
			packetver: 20211103,             // must match the pre-renewal server build
			renewal: false,
			packetKeys: false,               // clients after 2018-03-07 don't obfuscate packets
			socketProxy: base.replace(/^http/, 'ws') + 'ws/',
			forceUseAddress: true,           // char/map hand out the public IP; stay on the proxy's address
			adminList: [2000000]
		}],
		remoteClient: base,
		skipServerList: true,
		skipIntro: true                      // straight to the login: no file box, no START NOW
	};
})();
