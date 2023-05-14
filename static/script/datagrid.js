function InitDeleteAction() {
    $('.delete-button').click(function () {
        debugger
        var employeeId = $(this).data('id');
        swal({
            title: "Are you sure?",
            text: "You will not be able to recover this file!",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        }).then((willDelete) => {
            if (willDelete) {
                $.ajax({
                    url: '/delete-employee/' + employeeId,
                    type: 'DELETE',
                    success: function (result) {
                        window.location.href='/home'
                    },
                    error: function (xhr, status, error) {
                        alert(xhr.responseText);
                    }
                });
            }
        });

    });
}

function InitEditAction() {
    $('.edit-button').click(function () {
        debugger
        var employeeId = $(this).data('id');
        window.location.href = "/registration?id=" + employeeId;
    })
}
function InitUpdateAction() {
    window.location.href = "/updateregistration";
}
function InitViewAction(){
$('.view-button').click(function() {
  debugger
      var email = $(this).closest('tr').find('td:eq(1)').text();
  $('#pdf-iframe').attr('src', '/view_pdf/'+email);
  $('#pdf-modal').modal('show');
  });
}

$(document).ready(function () {
    $('#employee-table').DataTable({
        ajax: '/get_all_employees',
        columns: [
            { data: 'name' },
            { data: 'email' },
            { data: 'country' },
            { data: 'city' },
            { data: 'zipcode' },
            { data: 'phone' },
            { data: 'department' },
            { data: 'skillpercent'},
            {
                data: null,
                render: function (data, type, row) {
                    return '<button  type="button" class="button edit-button" data-id="' + data.id + '">Edit</button>';
                }
            },
            {
                data: null,
                render: function (data, type, row) {
                    return '<button type="button" class="button view-button" data-id="' + data.id + '">View</button>';
                }
            },
            {
                data: null,
                render: function (data, type, row) {
                    return '<button type="button" class="button delete-button" data-id="' + data.id + '">Delete</button>';
                }
            }

        ],
        initComplete: function () {
            InitDeleteAction();
            InitEditAction();
            InitViewAction();
            $('.paginate_button').click(function(){
            InitDeleteAction();
            InitEditAction();
            InitViewAction();
            })
        }
    });
});