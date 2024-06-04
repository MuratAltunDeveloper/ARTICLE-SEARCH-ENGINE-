is_correction = False
    
async with httpx.AsyncClient(http2=True) as client:
    response = await client.get(f"https://scholar.google.com/scholar?q={quote_plus(query)}&hl=tr&as_sdt=0,5&as_rr=1")

    if response.status_code == 200:
        selector = BeautifulSoup(response.content, "html.parser")
        correction = selector.select_one("div#gs_res_ccl_top")

        if correction:
            correction_text = correction.select_one("h2.gs_rt a")
            query = correction_text.text if correction_text else query
            is_correction=True
            