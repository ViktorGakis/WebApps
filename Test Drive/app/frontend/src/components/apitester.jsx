import React, { useState, useEffect } from 'react';

import { fetchAPI } from '../js/utils.js'

export default ApiTester;

function ApiTester({ endpoint }) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchDataAsync() {
            try {
                const response = await fetchAPI(endpoint);
                setData(response);
                setLoading(false);
            } catch (error) {
                setLoading(false);
            }
        }

        fetchDataAsync();
    }, [endpoint]);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (!data) {
        return <div>Error retrieving data.</div>;
    }

    return (
        <><div>
            {/* Render the data here */}
            {data &&
                <pre>
                    {JSON.stringify(data, null, 2)}
                </pre>}
        </div>
            <select>
                {data.map((item, index) => (
                    <option key={index} value={item.split('_')[0]}>
                        {item.split('_')[0]+'. '+item.split('_')[1]}
                    </option>
                ))}
            </select></>
    );
}


