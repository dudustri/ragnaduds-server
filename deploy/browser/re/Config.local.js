// RagnaDuds: roBrowser settings, the same on your PC (http://127.0.0.1:3339/) and on the site (/play-renewal/).
// Every URL is built from the page's own address, so the GRF files and the game proxy are always this server.
(function () {
	var base = location.origin + location.pathname.replace(/[^/]*$/, ''); // ".../" or ".../play-renewal/"
	window.ROConfigLocal = {
		servers: [{
			display: 'RagnaDuds Renewal',
			desc: 'Renewal · 3rd and 4th jobs',
			address: 'host.docker.internal', // the game servers, as the proxy container sees them
			port: 6901,
			langtype: 0,
			packetver: 20260107,             // must match the renewal server build
			renewal: true,
			packetKeys: false,               // clients after 2018-03-07 don't obfuscate packets
			socketProxy: base.replace(/^http/, 'ws') + 'ws/',
			forceUseAddress: true,           // char/map hand out the public IP; stay on the proxy's address
			adminList: [2000000]
		}],
		remoteClient: base,
		skipServerList: true,
		skipIntro: true,                     // straight to the login: no file box, no START NOW
		loadLua: true,                       // item names/pictures from the client's item list, like the exe:
		customItemInfo: ['System/itemInfo_browser.lua']   // made by client/browser_data.py from the download
	};
})();
