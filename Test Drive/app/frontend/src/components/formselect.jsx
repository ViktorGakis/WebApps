import React, { useState } from 'react';

function actualSelectForm(data, selectedOption, setSelectedOption, handleSubmit, method, url) {
    const handleFormSubmit = async (e) => {
        e.preventDefault();
        await handleSubmit(e, selectedOption); // Pass the event object and selectedOption as arguments to the handleSubmit function
    };

    return (
        <form onSubmit={ handleFormSubmit } method={ method } action={ url }>
            <select value={ selectedOption } onChange={ (e) => setSelectedOption(e.target.value) }>
                { data.map((item, index) => {
                    return (
                        <option key={ index } value={ item }>
                            { item }
                        </option>
                    );
                }) }
            </select>
            <button type="submit">Submit</button>
        </form>
    );
}

function FormSelect({ data, url, method, handleSubmit }) {
    const [selectedOption, setSelectedOption] = useState('');

    return actualSelectForm(
        data,
        selectedOption,
        setSelectedOption,
        handleSubmit,
        method,
        url
    );
}


export { FormSelect };