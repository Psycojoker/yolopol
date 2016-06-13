function selectPage(querystring, currentPage, lastPage, promptText) {
	var page = prompt(promptText + ' (1 to ' + lastPage + ')', currentPage);
	var npage = Number(page);

	if (page !== null && !isNaN(npage) && npage > 0 && npage <= lastPage) {
		location.href = '?' + querystring + '&page=' + npage;
	}
}
