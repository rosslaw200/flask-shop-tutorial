document.addEventListener('DOMContentLoaded', function () {
    // the menu button thing
    const menuBtn = document.getElementById('hamburger');
    if (menuBtn) {
        menuBtn.onclick = function () {
            document.getElementById('nav-links').classList.toggle('active');
        };
    }

    // the search bar stuff
    const searchThing = document.getElementById('search-btn');
    if (searchThing) {
        searchThing.onclick = function () {
            const formObj = document.getElementById('search-form');
            const inputObj = document.getElementById('search-input');
            if (!formObj.classList.contains('expanded')) {
                formObj.classList.add('expanded');
                inputObj.focus();
            } else {
                if (inputObj.value.trim() !== '') {
                    formObj.submit();
                } else {
                    formObj.classList.remove('expanded');
                }
            }
        };
    }

    // show/hide password buttons
    const passButtons = document.querySelectorAll('.showPwdBtn');
    passButtons.forEach(btn => {
        btn.onclick = function () {
            const field = this.previousElementSibling;
            if (field && (field.type === 'password' || field.type === 'text')) {
                // we dont use icons anymore so just swap type
                if (field.type === 'password') {
                    field.type = 'text';
                    this.textContent = 'Hide';
                } else {
                    field.type = 'password';
                    this.textContent = 'Show';
                }
            }
        };
    });

    // faq accordion
    const faqItems = document.querySelectorAll('.faq-question');
    faqItems.forEach(item => {
        item.addEventListener('click', () => {
            const parent = item.parentElement;
            parent.classList.toggle('active');
        });
    });
});

// stuff for the producer dashboard
function selectThing(the_row) {
    // get the data from the row
    const the_id = the_row.dataset.id;
    const the_name = the_row.dataset.name;
    const the_price = the_row.dataset.price;

    // take off the green from everything
    const allRows = document.querySelectorAll('#inventoryTable tbody tr');
    allRows.forEach(r => r.classList.remove('highlighted'));

    // highlight the one we clicked
    the_row.classList.add('highlighted');

    // put the data in the boxes
    document.getElementById('update_id').value = the_id;
    document.getElementById('update_name').value = the_name;
    document.getElementById('update_price').value = the_price;

    document.getElementById('stock_id').value = the_id;
    document.getElementById('stock_name_display').innerText = the_name;

    document.getElementById('delete_id').value = the_id;
    document.getElementById('delete_name_display').innerText = the_name;

    // hide the little hints
    document.getElementById('updateHint').style.display = 'none';
    document.getElementById('stockHint').style.display = 'none';
}

function popOpen(the_box) {
    document.getElementById(the_box).style.display = 'block';
}

function shutIt(the_box) {
    document.getElementById(the_box).style.display = 'none';
}

// close if click outside
window.onclick = function (event) {
    if (event.target.className === 'modal') {
        event.target.style.display = 'none';
    }
}
