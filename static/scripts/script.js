//const header = document.querySelectorAll('th');
//console.log(header)
//for (let i = 0; i < header.length; i++) {
//    header[i].addEventListener('click', order);
//}
//
//function order(e) {
//    switch (e.target.textContent) {
//        case 'fio':
//            selectOrd(e.target.textContent);
//            arr = arr.sort(sorterName);
//            break;
//        case 'age':
//            selectOrd(e.target.textContent);
//            arr = arr.sort(sorterName);
//            break;
//        default:
//            selectOrd(e.target.textContent);
//            const sortBnd = sortString.bind({orderBy: e.target.textContent});
//            arr = arr.sort(sortBnd);
//    }
//    buildTable(arr);
//}
//
//
//// Порядок сортировки
//let ordASC = 1;
//// Сортируемое поле
//let ordField = 'fio';
//
//function selectOrd(id) {
//    if (id === ordField) {
//        ordASC *= -1;
//    } else {
//        ordField = id;
//        ordASC = 1;
//    }
//}