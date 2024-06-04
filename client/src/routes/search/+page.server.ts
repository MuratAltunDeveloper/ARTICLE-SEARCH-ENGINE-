import type { PageServerLoad, Actions } from './$types';
import { getResults, setResultsOrdered, setResults, setResultsFiltered } from "$lib/server/database";
import type { Cookies } from '@sveltejs/kit';

function getUserid(cookies: Cookies) {
    let userid = cookies.get("userid");

    if (!userid) {
        userid = crypto.randomUUID();

        cookies.set("userid", userid, { path: "/" })
    }

    return userid;
}

export const load: PageServerLoad = async ({ cookies, url }) => {
    const userid = getUserid(cookies);
    const results = getResults(userid);
    
	return results;
};

export const actions = {
    default: async ({ request, cookies }) => {
        const formData = await request.formData();

        const pubtypes = formData.getAll("pubtypes") as string[];
        const publishers = formData.getAll("publishers") as string[];
        const authors = formData.getAll("authors") as string[];
        const min_years = formData.get("min-years") as string;
        const max_years = formData.get("max-years") as string;
        const min_citations = formData.get("min-citations") as string;
        const max_citations = formData.get("max-citations") as string;

        if (pubtypes.length > 0 || publishers.length > 0 || authors.length > 0 || min_years || max_years || min_citations || max_citations) {
            const userid = getUserid(cookies);

            await setResultsFiltered(userid, authors, pubtypes, publishers, `${min_years}-${max_years}`, `${min_citations}-${max_citations}`);

            return;
        }

        const query = formData.get("query") as string;
        const sort_param = formData.get("sort_by");
        const sort_value = formData.get("sort_order");

        if (sort_param && sort_value) {
            const userid = getUserid(cookies);

            await setResultsOrdered(userid, sort_param as string, sort_value as string);
        }
        else {
            const userid = getUserid(cookies);
        
            await setResults(userid, query);
        }
    },
} satisfies Actions;