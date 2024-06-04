<script lang="ts">
    import logoIcon from "$lib/icons/logo.svg?raw";

    let { data } = $props();

    let menuIsOpen: string = $state("none");

    function menuBtnHandler() {
        menuIsOpen = (menuIsOpen === "block") ? "none" : "block";
    }
</script>

<header class="bg-white">
    <nav class="mx-auto flex max-w-7xl items-center justify-between p-6 lg:px-8" aria-label="Global">
        <div class="flex lg:flex-1">
            <a href="/" class="-m-1.5 p-1.5">
                <span class="sr-only">Campus</span>
                {@html logoIcon}
            </a>
        </div>
        <div class="flex lg:hidden">
            <button onclick={menuBtnHandler} type="button" class="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700">
                <span class="sr-only">Open main menu</span>
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                    aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round"
                        d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                </svg>
            </button>
        </div>
        <div class="hidden lg:flex lg:gap-x-12">
            <a href="/articles" class="text-sm font-semibold leading-6 text-gray-900">Makaleler</a>
            <a href="/journals" class="text-sm font-semibold leading-6 text-gray-900">Dergiler</a>
        </div>
        <div class="hidden lg:flex lg:flex-1 lg:justify-end">
            <a href="/about" class="text-sm font-semibold leading-6 text-gray-900">Hakkımızda <span
                    aria-hidden="true">&rarr;</span></a>
        </div>
    </nav>
    <!-- Mobile menu, show/hide based on menu open state. -->
    <div class="lg:hidden" role="dialog" aria-modal="true" style="display: {menuIsOpen};">
        <!-- Background backdrop, show/hide based on slide-over state. -->
        <div class="fixed inset-0 z-10"></div>
        <div
            class="fixed inset-y-0 right-0 z-10 w-full overflow-y-auto bg-white px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10">
            <div class="flex items-center justify-between">
                <a href="/" class="-m-1.5 p-1.5">
                    <span class="sr-only">Campus</span>
                    {@html logoIcon}
                </a>
                <button onclick={menuBtnHandler} type="button" class="-m-2.5 rounded-md p-2.5 text-gray-700">
                    <span class="sr-only">Close menu</span>
                    <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                        aria-hidden="true">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
            <div class="mt-6 flow-root">
                <div class="-my-6 divide-y divide-gray-500/10">
                    <div class="space-y-2 py-6">
                        <a href="/articles"
                            class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50">Makaleler</a>
                        <a href="/journals"
                            class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50">Dergiler</a>
                    </div>
                    <div class="py-6">
                        <a href="/about"
                            class="-mx-3 block rounded-lg px-3 py-2.5 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50">Hakkımızda</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</header>

<main>
    <div class="w-full">
        <div class="bg-gray-100">
            <div class="flex flex-col text-gray-500 max-w-7xl mx-auto py-10 px-6 lg:px-8">
                <div class="text-sm">
                    <p>DOI: <span>{data.article.doi}</span></p>
                </div>
                <div class="text-3xl font-bold text-slate-800 my-2">
                    <h1>{data.article.title}</h1>
                </div>
                <div class="flex items-center text-sm font-medium flex-wrap max-w-lg">
                    {#each data.article.authors as author}
                        <p class="mr-5 text-indigo-700">{author}</p>
                    {/each}
                </div>
                <div class="text-sm font-semibold mt-2">
                    <p>Yayınlama tarihi: {data.article.pubdates}</p>
                </div>
                <div class="text-gray-700 mt-3">
                    <p><span class="py-1 px-2 bg-white text-slate-800 font-medium rounded-lg mr-2">Abstract</span> {data.article.abstract}</p>
                </div>
                <div class="flex items-center mt-5">
                    <a class="px-10 py-1 bg-red-500 text-sm text-white font-bold rounded" target="_blank" href={data.article.pdf_url}>PDF</a>
                </div>
            </div>
        </div>
        <div class="flex flex-col max-w-7xl mx-auto py-10 px-6 lg:px-8">
            <div>
                <div id="accordion-collapse" data-accordion="collapse">
                    <h2 id="accordion-collapse-heading-1">
                    <button type="button" class="flex items-center justify-between w-full p-5 font-medium rtl:text-right text-gray-500 border border-b-0 border-gray-200 rounded-t-xl focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-800 dark:border-gray-700 dark:text-gray-400 bg-gray-100 dark:hover:bg-gray-800 gap-3" data-accordion-target="#accordion-collapse-body-1" aria-expanded="true" aria-controls="accordion-collapse-body-1">
                        <span>Anahtar kelimeler</span>
                    </button>
                    </h2>
                    <div id="accordion-collapse-body-1" aria-labelledby="accordion-collapse-heading-1">
                        <div class="p-5 border border-b-0 border-gray-200 dark:border-gray-700 dark:bg-gray-900">
                            {#each data.article.keywords as keyword}
                                <span class="px-3 py-1 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-400 rounded-lg mr-2">{keyword}</span>
                            {/each}
                        </div>
                    </div>
                    <h2 id="accordion-collapse-heading-1">
                    <button type="button" class="flex items-center justify-between w-full p-5 font-medium rtl:text-right text-gray-500 border border-gray-200 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-800 dark:border-gray-700 dark:text-gray-400 bg-gray-100 dark:hover:bg-gray-800 gap-3" data-accordion-target="#accordion-collapse-body-1" aria-expanded="true" aria-controls="accordion-collapse-body-1">
                        <span>Referanslar</span>
                    </button>
                    </h2>
                    <div id="accordion-collapse-body-1" aria-labelledby="accordion-collapse-heading-1">
                        <div class="flex flex-col gap-5 p-5 border border-gray-200 dark:border-gray-700 dark:bg-gray-900">
                            {#each data.article.references as reference}
                                <div class="relative pl-7">
                                    <span class="absolute text-2xl text-indigo-500 font-bold left-0 top-px">&#8220;</span>
                                    <p class="text-gray-500 dark:text-gray-400">{reference}</p>
                                </div>
                            {/each}
                        </div>
                    </div>
                </div>
            </div>
            <div class="relative overflow-x-auto mt-5">
                <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
                    <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                        <tr>
                            <th scope="col" class="px-6 py-3">
                                Özellik
                            </th>
                            <th scope="col" class="px-6 py-3">
                                Ayrıntı
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                            <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                                Yayın türü
                            </th>
                            <td class="px-6 py-4">
                                {data.article.pubtype}
                            </td>
                        </tr>
                        <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                            <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                                Atıf sayısı
                            </th>
                            <td class="px-6 py-4">
                                {data.article.citations}
                            </td>
                        </tr>
                        <tr class="bg-white dark:bg-gray-800">
                            <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                                Yayıncı
                            </th>
                            <td class="px-6 py-4">
                                {data.article.publisher}
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</main>