let counter = 1;

let clothing = ['Shoes', 'Socks', 'Dresses and Skirts', 'Pants', 'Hats', 'Jackets and Sweaters', 'Shirts', 'Shorts'].map((item) => {
    let ref = item.toLowerCase().replace(/\s+/g, '');
    let result = {
        name: item,
        index: counter,
        ref: ref + '.png',
        large_ref: ref + '@2x.png'
    };
    counter = counter+1;
    return result;
});

let hygiene = ['Toothpaste', 'Soap', 'Toothbrush', 'Mouthwash'].map((item) => {
    let ref = item.toLowerCase().replace(/\s+/g, '');
    let result = {
        name: item,
        index: counter,
        ref: ref + '.png',
        large_ref: ref + '@2x.png'
    };

    counter = counter+1;
    return result;
});


let essentials = ['Feminine Hygiene', 'Sleeping Bags', 'Dog Food', 'Cat Food', 'Blankets'].map((item) => {
    let ref = item.toLowerCase().replace(/\s+/g, '');
    let result = {
        name: item,
        index: counter,
        ref: ref + '.png',
        large_ref: ref + '@2x.png'
    };

    counter = counter+1;
    return result;
});


export const ITEMS = {
    clothing: clothing,
    essentials: essentials,
    hygiene: hygiene
}
   
    
