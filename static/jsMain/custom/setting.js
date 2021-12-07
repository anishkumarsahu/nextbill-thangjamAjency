

function delCompany(id) {
   $('#deleteCompany')
  .modal('show')
;
   $('#companyID').val(id)
}

function deleteCompany() {
    var id = $('#companyID').val();
    var formdata = new FormData();
    formdata.append('companyID', id);
    debugger;

     $.ajax({
                    url: "/api/delete_company/",
                    type: "post",
                    data: formdata,
             contentType: false,
                         cache: false,
                         processData: false,

                     success: function (response) {
                         if (response.message === 'success') {
                             $('body')
                                 .toast({
                                     class: 'success',
                                     message: 'Company Deleted Successfully.'
                                 })
                             ;


                             productTab.ajax.reload();
                         } else {
                             $('body')
                                 .toast({
                                     class: 'error',
                                     message: 'An error occurred !'
                                 })
                             ;

                         }

                         return response;
                     },
                     error: function () {
                         $('body')
                             .toast({
                                 class: 'error',
                                 message: 'An error occurred !'
                             })
                         ;
                     }
                            });

}

        function showModal(){
            $('#myModal').modal('show');
        }

        function ShowBankDetails(){
            $('#BankDetails').modal('show');
        }

        function EditCompanyModal(){
            $('#editCompany').modal('show');
        }



        //POST COMPANY
    function addCompany() {
            //for Company
             var companyName = $('#companyName').val();
             var gstNo = $('#gstNo').val();
             var companyPhone = $('#companyPhone').val();
             var companyEmail = $('#companyEmail').val();
             var companyAddress = $('#companyAddress').val();
             var state = $('#state').val();
             var city = $('#city').val();
             var zip = $('#zip').val();

            //for Bank
             var accountHolderName = $('#accountHolderName').val();
             var bankName = $('#bankName').val();
             var branch = $('#branch').val();
             var account_type = $('#account_type').val();
             var accountNo = $('#accountNo').val();
             var ifsc = $('#ifsc').val();
             var bankAddress = $('#bankAddress').val();


             if (companyName === '' || gstNo === '' || companyPhone === '' ||
                 companyEmail === '' || companyAddress === '' || state === '') {
                 $('body')
                     .toast({
                         class: 'orange',
                         message: 'Company Name, GST.No, Phone Number, Email, Address ... are required !'
                     })
                 ;
             } else {

                 var csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();

                 data = new FormData();
                 data.append('companyName', companyName);
                 data.append('gstNo', gstNo);
                 data.append('companyPhone', companyPhone);
                 data.append('companyEmail', companyEmail);
                 data.append('companyAddress', companyAddress);
                 data.append('state', state);
                 data.append('city', city);
                 data.append('zip', zip);

                 data.append('accountHolderName', accountHolderName);
                 data.append('bankName', bankName);
                 data.append('branch', branch);
                 data.append('account_type', account_type);
                 data.append('accountNo', accountNo);
                 data.append('ifsc', ifsc);
                 data.append('bankAddress', bankAddress);

                 data.append('csrfmiddlewaretoken', csrfmiddlewaretoken);

                 $.ajax({
                     type: 'post',
                     url: '/api/PostCompanyDetail/',
                     data: data,
                     contentType: false,
                     cache: false,
                     processData: false,


                     success: function (response) {
                         if (response.message === 'success') {
                             $('#myModal').modal('hide');
                             $("#AddCompanyForm")[0].reset();
                             $('body')
                                 .toast({
                                     class: 'success',
                                     message: 'Company Added Successfully.'
                                 })
                             ;


                             productTab.ajax.reload();
                             $('#AddCompanyForm').trigger('reset')
                            $('#myModal').modal('toggle');
                         } else {
                             $('body')
                                 .toast({
                                     class: 'error',
                                     message: 'An error occurred !'
                                 })
                             ;

                         }

                         return response;
                     },
                     error: function () {
                         $('body')
                             .toast({
                                 class: 'error',
                                 message: 'An error occurred !'
                             })
                         ;
                     }
                 });


             }

         }




        function deleteIns(id) {
            $.confirm({
                title: 'Delete!',
                content: 'Please Confirm !',
                type: 'red',
                typeAnimated: true,
                buttons: {
                    tryAgain: {
                        text: 'Delete',
                        btnClass: 'btn-red',
                        action: function () {
                            var formData = {
                                'ID': id
                            };

                        }
                    },
                    close: function () {


                    }
                }
            });
        }


        function GetBankDetails(id){
                ShowBankDetails();
                $.ajax({
                type: 'get',
                url: '/api/get_bank_detail/'+id+'/',

                success: function (response) {
                    console.log(response);
                    $('#AccHolder').html(response.data['AccHolder']);
                    $('#AccNumber').html(response.data['AccNumber']);
                    $('#Branch').html(response.data['Branch']);
                    $('#AccType').html(response.data['AccType']);
                    $('#ifscCode').html(response.data['ifscCode']);
                    $('#HolderAddress').html(response.data['HolderAddress']);


                },
                error: function () {
                    $('body')
                        .toast({
                            class: 'error',
                            message: 'An error occurred !'
                        })
                    ;
                }
            });
            };

        function GetCompanyDetails(id){
                EditCompanyModal();
                $.ajax({
                type: 'get',
                url: '/api/get_Company_detail/'+id+'/',

                success: function (response) {
                    console.log(response);
                    $('#EcompId').val(response.data['ID']);
                    $('#EditCompanyName').val(response.data['EditCompanyName']);
                    $('#EditGstNo').val(response.data['EditGstNo']);
                    $('#EditCompanyPhone').val(response.data['EditCompanyPhone']);
                    $('#EditCompanyEmail').val(response.data['EditCompanyEmail']);
                    $('#EditCompanyAddress').val(response.data['EditCompanyAddress']);
                    $('#EditZip').val(response.data['EditZip']);
                    $('#EditState').val(response.data['EditState']);
                    $('#EditCity').val(response.data['EditCity']);
                    $('#EditAccountHolderName').val(response.data['EditAccountHolderName']);
                    $('#EditBankName').val(response.data['EditBankName']);
                    $('#EditBranch').val(response.data['EditBranch']);
                    $('#EditAccount_type').val(response.data['EditAccount_type']);
                    $('#EditAccountNo').val(response.data['EditAccountNo']);
                    $('#EDitIfsc').val(response.data['EDitIfsc']);
                    $('#EditBankAddress').val(response.data['EditBankAddress']);


                },
                error: function () {
                    $('body')
                        .toast({
                            class: 'error',
                            message: 'An error occurred !'
                        })
                    ;
                }
            });
            };

        var re = $('#EcompId').val();
                    console.log(re+'=test');


    function EditCompany() {
            //for Company
             var ID = $('#EcompId').val();
             var companyName = $('#EditCompanyName').val();
             var gstNo = $('#EditGstNo').val();
             var companyPhone = $('#EditCompanyPhone').val();
             var companyEmail = $('#EditCompanyEmail').val();
             var companyAddress = $('#EditCompanyAddress').val();
             var state = $('#EditState').val();
             var city = $('#EditCity').val();
             var zip = $('#EditZip').val();

            //for Bank
             var accountHolderName = $('#EditAccountHolderName').val();
             var bankName = $('#EditBankName').val();
             var branch = $('#EditBranch').val();
             var account_type = $('#EditAccount_type').val();
             var accountNo = $('#EditAccountNo').val();
             var ifsc = $('#EDitIfsc').val();
             var bankAddress = $('#EditBankAddress').val();


             if (companyName === '' || gstNo === '' || companyPhone === '' ||
                 companyEmail === '' || companyAddress === '' || state === '') {
                 $('body')
                     .toast({
                         class: 'orange',
                         message: 'Company Name, GST.No, Phone Number, Email, Address ... are required !'
                     })
                 ;
             } else {

                 var csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();

                 data = new FormData();
                 data.append('companyID', ID);
                 data.append('companyName', companyName);
                 data.append('gstNo', gstNo);
                 data.append('companyPhone', companyPhone);
                 data.append('companyEmail', companyEmail);
                 data.append('companyAddress', companyAddress);
                 data.append('state', state);
                 data.append('city', city);
                 data.append('zip', zip);

                 data.append('accountHolderName', accountHolderName);
                 data.append('bankName', bankName);
                 data.append('branch', branch);
                 data.append('account_type', account_type);
                 data.append('accountNo', accountNo);
                 data.append('ifsc', ifsc);
                 data.append('bankAddress', bankAddress);

                 data.append('csrfmiddlewaretoken', csrfmiddlewaretoken);

                 $.ajax({
                     type: 'post',
                     url: '/api/EditCompanyDetail/',
                     data: data,
                     contentType: false,
                     cache: false,
                     processData: false,


                     success: function (response) {
                         if (response.message === 'success') {
                             $('#myModal').modal('hide');
                             $("#AddCompanyForm")[0].reset();
                             $('body')
                                 .toast({
                                     class: 'success',
                                     message: 'Company Edited Successfully.'
                                 })
                             ;


                             productTab.ajax.reload();
                             $('#EditCompanyForm').trigger('reset');
                            $('#editCompany').modal('toggle');
                         } else {
                             $('body')
                                 .toast({
                                     class: 'error',
                                     message: 'An error occurred !'
                                 })
                             ;

                         }

                         return response;
                     },
                     error: function () {
                         $('body')
                             .toast({
                                 class: 'error',
                                 message: 'An error occurred !'
                             })
                         ;
                     }
                 });


             }

         }
