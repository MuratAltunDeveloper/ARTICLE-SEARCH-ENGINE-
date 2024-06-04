<script lang="ts">
    import logoIcon from "$lib/icons/logo.svg?raw";

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

<main class="h-max-screen" style="height: calc(100vh - 5rem);">
    <div class="h-full mx-auto flex max-w-7xl items-center justify-between p-6 lg:px-8">
        <form class="mx-auto w-full pb-20 md:w-2/3 lg:w-1/2" action="/search" method="post">
            <div class="flex flex-col gap-5 lg:gap-10">
                <div class="flex justify-center">
                    <h1 class="text-3xl md:text-5xl lg:text-7xl text-blue-700 font-semibold">
                        Campus
                    </h1>
                </div>
                <div class="relative mt-2 rounded-3xl shadow-sm">
                    <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-5">
                        <span class="text-gray-500 sm:text-sm">
                            <i class="fi fi-rr-search"></i>
                        </span>
                    </div>
                    <input type="text" name="query" id="query" class="block w-full rounded-3xl border-2 py-2.5 pl-11 pr-20 text-gray-800 placeholder:text-gray-500 outline-none focus:border-indigo-700 sm:text-sm sm:leading-6" placeholder="Makale ara" required>
                </div>
                <div class="mx-auto">
                    <button class="border border-transparent bg-gray-50 hover:border-gray-300 text-sm text-gray-700 py-2 px-4 rounded">
                        Campus'de ara
                    </button>
                </div>
            </div>
        </form>
    </div>
</main>

<style lang="postcss">
    :global(i) {
        display: flex;
        align-items: center;
    }
</style>