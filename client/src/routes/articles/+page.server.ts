import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ url }) => {
    const sort_param = url.searchParams.get("sort_by");
    const sort_value = url.searchParams.get("sort_order");
    
    let uri = "";

    if (sort_param && sort_value) {
        uri = `http://localhost:8000/articles?sort_by=${sort_param}&sort_order=${sort_value}`;
    }
    else {
        uri = `http://localhost:8000/articles`;
    }

    const response = await fetch(uri);

    const results = await response.json();

    console.log(results);
    
    return results;
};