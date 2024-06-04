<script lang="ts">
    import SearchResults from "$lib/components/SearchResults.svelte";

    let { data } = $props();
    
    let authors: string[] = $state([]);
    let pubtypes: string[] = $state([]);
    let publishers: string[] = $state([]);

    let min_years: number = $state(2150);
    let max_years: number = $state(0);

    let selected_min_years = $state(0);
    let selected_max_years = $state(0);

    let min_citations: number = $state(2150);
    let max_citations: number = $state(0);

    let selected_min_citations = $state(0);
    let selected_max_citations = $state(0);

    for (const iterator of data.results) {
        for (const author of iterator.authors) {
            if (!authors.includes(author)) {
                authors.push(author);
            }
        }

        if (!pubtypes.includes(iterator.pubtype)) {
            pubtypes.push(iterator.pubtype);
        }

        if (!publishers.includes(iterator.publisher)) {
            publishers.push(iterator.publisher);
        }

        const parts = iterator.pubdates.split(' ');
        const years = (parts.length === 3) ? parseInt(parts[2]) : 2024;
        
        if (years < min_years) {
            min_years = years;
        }

        if (years > max_years) {
            max_years = years;
        }

        if (iterator.citations < min_citations) {
            min_citations = iterator.citations;
        }

        if (iterator.citations > max_citations) {
            max_citations = iterator.citations;
        }
    }
    
    $effect(() => {
        selected_min_years = min_years;
        selected_max_years = max_years;
    });

    $effect(() => {
        selected_min_citations = min_citations;
        selected_max_citations = max_citations;
    });

    function toggle_order_menu() {
        const menu = document.getElementById('menu');
        menu?.classList.toggle('hidden');
    }
</script>

<div class="flex flex-col min-h-full">
    <div class="w-full flex relative items-center px-10 py-7 md:px-28">
        <div class="absolute left-20">
            <a href="/">
                <svg width="23.39" height="32" viewBox="0 0 23.39 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <g clip-path="url(#clip0_2630_43809)">
                        <path
                            d="M21.213 13.3064C20.4276 12.7316 18.1486 11.085 17.1785 10.386C17.8868 8.65398 18.5413 7.11611 18.9724 6.02097C19.4036 4.92582 18.9955 3.64427 17.9869 2.8365C17.3786 2.34718 16.3623 1.63262 15.7233 1.19767C12.9438 -0.713014 9.84089 -0.231461 8.2394 1.95883C5.89107 5.15883 3.34256 8.68504 1.10972 11.8229C-0.799742 14.5025 -0.152989 17.7491 2.38783 19.6365C2.98838 20.0792 3.92002 20.7938 4.91324 21.5161C4.33579 22.3161 3.74293 23.1394 3.18087 23.9161C2.22614 25.2443 2.45712 26.7355 3.78143 27.7297C5.483 28.9957 7.02289 30.1219 8.2548 30.9763C10.5723 32.5841 13.6444 32.3588 15.5154 29.92C17.7867 26.953 21.0051 22.3239 22.3525 20.4598C24.108 18.0287 23.5767 15.0384 21.2053 13.3142L21.213 13.3064ZM3.11927 13.687C3.61974 13.0035 9.58681 4.70834 10.2644 3.79961C11.196 2.55689 12.4356 2.35495 14.0371 3.38796C14.6838 3.80737 15.1689 4.12582 15.6001 4.52194C15.8696 4.77048 16.2083 5.2132 15.985 5.81902C15.5693 6.953 9.53291 21.4462 9.53291 21.4462C9.53291 21.4462 4.48978 17.7569 3.52734 17.0501C2.49562 16.2889 2.25694 14.852 3.11158 13.6792L3.11927 13.687ZM20.1966 18.7977C18.4874 21.1666 15.3383 25.8268 13.2748 28.3821C12.4202 29.4384 11.1036 29.586 10.1797 28.9491C9.17104 28.2579 6.78421 26.5336 5.39061 25.5161C5.99117 24.6928 6.55323 23.9006 7.12298 23.1161C8.02382 23.7608 8.74757 24.2656 8.97085 24.4054C9.89478 24.9724 11.1344 24.8015 11.6734 23.7064C11.9351 23.1705 14.1064 17.8889 16.1159 12.9802C17.0014 13.6171 18.7029 14.852 19.727 15.6054C20.7048 16.3278 21.0128 17.6637 20.1966 18.7899V18.7977Z"
                            fill="#6E32FF"></path>
                    </g>
                    <defs>
                        <clipPath id="clip0_2630_43809">
                            <rect width="83" height="32" fill="white"></rect>
                        </clipPath>
                    </defs>
                </svg>
            </a>
        </div>
        <div class="w-full h-full flex items-center pl-16">
            <form action="/search" method="post" class="w-full max-w-2xl">
                <label for="default-search"
                    class="mb-2 text-sm font-medium text-gray-800 sr-only dark:text-white">Ara</label>
                <div class="relative">
                    <div class="absolute inset-y-0 start-0 flex items-center ps-5 pointer-events-none">
                        <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
                        </svg>
                    </div>
                    <input type="text" name="query" id="query" class="block w-full rounded-3xl border-2 py-2.5 pl-11 pr-20 text-gray-800 placeholder:text-gray-500 outline-none focus:border-indigo-700 sm:text-sm sm:leading-6" placeholder="Makale ara" value={data.query} required>
                </div>
            </form>
        </div>
    </div>
    <div class="flex px-10 pb-10 md:px-28">
        <div class="w-2/3 px-11">
            <div class="flex items-center">
                <div class="ml-auto">
                    <div class="relative inline-block text-left">
                        <div>
                            <button onclick={toggle_order_menu} type="button"
                                class="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                                id="menu-button" aria-expanded="false" aria-haspopup="true">
                                Sırala
                                <svg class="-mr-1 h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor"
                                    aria-hidden="true">
                                    <path fill-rule="evenodd"
                                        d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"
                                        clip-rule="evenodd" />
                                </svg>
                            </button>
                        </div>
                        <div id="menu"
                            class="hidden absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
                            role="menu" aria-orientation="vertical" aria-labelledby="menu-button" tabindex="-1">
                            <div class="py-1" role="none">
                                <form action="/search" method="post">
                                    <input class="hidden" type="text" name="sort_by" id="sort_by" value="citations">
                                    <input class="hidden" type="number" name="sort_order" id="sort_order" value="1">
                                    <button type="submit" class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem" tabindex="-1">Atıf Sayısına Göre Artan</button>
                                </form>
                                <form action="/search" method="post">
                                    <input class="hidden" type="text" name="sort_by" id="sort_by" value="citations">
                                    <input class="hidden" type="number" name="sort_order" id="sort_order" value="-1">
                                    <button type="submit" class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem" tabindex="-1">Atıf Sayısına Göre Azalan</button>
                                </form>
                                <form action="/search" method="post">
                                    <input class="hidden" type="text" name="sort_by" id="sort_by" value="pubdates_timestamp">
                                    <input class="hidden" type="number" name="sort_order" id="sort_order" value="1">
                                    <button type="submit" class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem" tabindex="-1">Tarihe Göre Artan</button>
                                </form>
                                <form action="/search" method="post">
                                    <input class="hidden" type="text" name="sort_by" id="sort_by" value="pubdates_timestamp">
                                    <input class="hidden" type="number" name="sort_order" id="sort_order" value="-1">
                                    <button type="submit" class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem" tabindex="-1">Tarihe Göre Azalan</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="mt-5">
                {#each data.results as article}
                    <SearchResults
                        id={article._id}
                        title={article.title}
                        abstract={article.abstract}
                        citations={article.citations}
                        pubtype={article.pubtype}
                        pdf_url={article.pdf_url}
                        pubdates={article.pubdates}
                        publisher={article.publisher}
                    />
                {/each}
            </div>
        </div>
        <div class="w-1/3">
            <form action="/search" method="post">
                <div class="flex flex-col rounded border border-gray-300 p-5 ml-5">
                    <h3 class="text-lg text-slate-800 font-semibold">Yazarlar</h3>
                    <div class="flex flex-col p-3 gap-2">
                        {#each authors as author}
                            <div class="flex items-center">
                                <input id={author} name="authors" type="checkbox" value={author} class="w-4 h-4 bg-blue-100 border-blue-300 rounded text-primary-600 focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500" />

                                <label for="apple" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-100">
                                    {author}
                                </label>
                            </div>
                        {/each}
                    </div>
                    <h3 class="text-lg text-slate-800 font-semibold">Yayıncılar</h3>
                    <div class="flex flex-col p-3 gap-2">
                        {#each publishers as publisher}
                            <div class="flex">
                                <input id={publisher} name="publishers" type="checkbox" value={publisher} class="w-4 h-4 bg-blue-100 border-blue-300 rounded text-primary-600 focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500" />

                                <label for="apple" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-100">
                                    {publisher}
                                </label>
                            </div>
                        {/each}
                    </div>
                    <h3 class="text-lg text-slate-800 font-semibold">Makale Türleri</h3>
                    <div class="flex flex-col p-3 gap-2">
                        {#each pubtypes as pubtype}
                            <div class="flex items-center">
                                <input id={pubtype} name="pubtypes" type="checkbox" value={pubtype} class="w-4 h-4 bg-blue-100 border-blue-300 rounded text-primary-600 focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500" />

                                <label for="apple" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-100">
                                    {pubtype}
                                </label>
                            </div>
                        {/each}
                    </div>
                    <h3 class="text-lg text-slate-800 font-semibold">Tarih Aralığı</h3>
                    <div class="flex flex-col p-3 gap-2">
                        <label for="minmax-range" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Minimum yıl</label>
                        <input bind:value={selected_min_years} id="minmax-range" name="min-years" type="range" min={min_years} max={max_years} class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700">
                        <p>{selected_min_years}</p>
                        <label for="minmax-range" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white mt-3">Maksimum yıl</label>
                        <input bind:value={selected_max_years} id="minmax-range" name="max-years" type="range" min={min_years} max={max_years} class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700">
                        <p>{selected_max_years}</p>
                    </div>
                    <h3 class="text-lg text-slate-800 font-semibold">Atıf Sayısı Aralığı</h3>
                    <div class="flex flex-col p-3 gap-2">
                        <label for="minmax-range" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Minimum yıl</label>
                        <input bind:value={selected_min_citations} id="minmax-range" name="min-citations" type="range" min={min_citations} max={max_citations} class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700">
                        <p>{selected_min_citations}</p>
                        <label for="minmax-range" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white mt-3">Maksimum yıl</label>
                        <input bind:value={selected_max_citations} id="minmax-range" name="max-citations" type="range" min={min_citations} max={max_citations} class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700">
                        <p>{selected_max_citations}</p>
                    </div>
                    <div class="mt-3">
                        <button type="submit" class="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 rounded">Filtrele</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
<footer class="px-44 py-7 bg-gray-50 dark:bg-gray-800">
    <div class="mx-auto">
        <div class="md:flex md:justify-between">
            <div class="mb-6 md:mb-0">
                <a href="https://flowbite.com" class="flex items-center">
                    <svg width="23.39" height="32" viewBox="0 0 23.39 32" fill="none"
                        xmlns="http://www.w3.org/2000/svg">
                        <g clip-path="url(#clip0_2630_43809)">
                            <path
                                d="M21.213 13.3064C20.4276 12.7316 18.1486 11.085 17.1785 10.386C17.8868 8.65398 18.5413 7.11611 18.9724 6.02097C19.4036 4.92582 18.9955 3.64427 17.9869 2.8365C17.3786 2.34718 16.3623 1.63262 15.7233 1.19767C12.9438 -0.713014 9.84089 -0.231461 8.2394 1.95883C5.89107 5.15883 3.34256 8.68504 1.10972 11.8229C-0.799742 14.5025 -0.152989 17.7491 2.38783 19.6365C2.98838 20.0792 3.92002 20.7938 4.91324 21.5161C4.33579 22.3161 3.74293 23.1394 3.18087 23.9161C2.22614 25.2443 2.45712 26.7355 3.78143 27.7297C5.483 28.9957 7.02289 30.1219 8.2548 30.9763C10.5723 32.5841 13.6444 32.3588 15.5154 29.92C17.7867 26.953 21.0051 22.3239 22.3525 20.4598C24.108 18.0287 23.5767 15.0384 21.2053 13.3142L21.213 13.3064ZM3.11927 13.687C3.61974 13.0035 9.58681 4.70834 10.2644 3.79961C11.196 2.55689 12.4356 2.35495 14.0371 3.38796C14.6838 3.80737 15.1689 4.12582 15.6001 4.52194C15.8696 4.77048 16.2083 5.2132 15.985 5.81902C15.5693 6.953 9.53291 21.4462 9.53291 21.4462C9.53291 21.4462 4.48978 17.7569 3.52734 17.0501C2.49562 16.2889 2.25694 14.852 3.11158 13.6792L3.11927 13.687ZM20.1966 18.7977C18.4874 21.1666 15.3383 25.8268 13.2748 28.3821C12.4202 29.4384 11.1036 29.586 10.1797 28.9491C9.17104 28.2579 6.78421 26.5336 5.39061 25.5161C5.99117 24.6928 6.55323 23.9006 7.12298 23.1161C8.02382 23.7608 8.74757 24.2656 8.97085 24.4054C9.89478 24.9724 11.1344 24.8015 11.6734 23.7064C11.9351 23.1705 14.1064 17.8889 16.1159 12.9802C17.0014 13.6171 18.7029 14.852 19.727 15.6054C20.7048 16.3278 21.0128 17.6637 20.1966 18.7899V18.7977Z"
                                fill="#6E32FF"></path>
                        </g>
                        <defs>
                            <clipPath id="clip0_2630_43809">
                                <rect width="83" height="32" fill="white"></rect>
                            </clipPath>
                        </defs>
                    </svg>
                    <span
                        class="self-center text-2xl ml-3 font-semibold whitespace-nowrap dark:text-white">Campus</span>
                </a>
            </div>
            <div class="grid">
                <div>
                    <h2 class="mb-6 text-sm font-semibold text-gray-900 uppercase dark:text-white">Bağlantılar</h2>
                    <ul class="text-gray-600 dark:text-gray-400">
                        <li class="mb-4">
                            <a href="/articles" class="hover:underline">Makaleler</a>
                        </li>
                        <li>
                            <a href="/journals" class="hover:underline">Dergiler</a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <hr class="my-6 border-gray-200 sm:mx-auto dark:border-gray-700 lg:my-8" />
        <div class="sm:flex sm:items-center sm:justify-between">
            <span class="text-sm text-gray-500 sm:text-center dark:text-gray-400">© 2024 <a href="https://flowbite.com"
                    class="hover:underline">Campus™</a>. Bütün Hakları Saklıdır.</span>
        </div>
    </div>
</footer>