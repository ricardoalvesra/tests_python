function loadCustomer() {
    $(function () {
        $("#jsGrid").jsGrid({
            height: "100%",
            width: "100%",

            //filtering: true,
            //editing: false,
            sorting: true,
            //paging: true,
            //autoload: true,

            pageSize: 15,
            pageButtonCount: 5,

            data: getCustomers(),
            fields: [
                { name: "name", type: "text", width: 50, title: "Name" },
                { name: "address", type: "text", width: 50, title: "Address" },
                { name: "postalcode", type: "text", width: 50, title: "Postal Code" },
                { name: "county", type: "text", width: 50, title: "County" },
                { name: "telephone", type: "text", width: 50, title: "Telephone" },
                { name: "email", type: "text", width: 50, title: "Email" }
            ],

            rowClick: function (e) {
                window.location = "/customer/" + e.item.id;
            }
        });
    });
}

function getCustomers() {
    var response = [];
    $.ajax({
        async: false,
        type: "GET",
        url: "/getcustomers",
        dataType: "json",
        success: function (data) {
            let obj = JSON.parse(data);
            obj.forEach(element => {
                element.fields["id"] = element.pk;
                response.push(element.fields);
            });
        },
        error: function (e) {
            console.log(e);
        }
    });

    return response;
}
