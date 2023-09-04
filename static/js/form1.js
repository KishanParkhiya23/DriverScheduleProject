const csrftoken = $("[name=csrfmiddlewaretoken]").val();
if ($(window).width() < 1000) {
    $("body #mainCont").addClass("container-fluid");
    $("body #mainCont").removeClass("container");
} else {
}

document
    .getElementById("nextBtn")
    .addEventListener("click", function (event) {
        event.preventDefault();

        if (checkData()) {
            $("#signUpForm").submit();
        }

    });

var driverId = document.getElementById("driverId");
var clientId = document.getElementById("clientId");
var shiftType = document.getElementById("shiftType");
var numberOfLogs = document.getElementById("numberOfLogs");
var truckNum = document.getElementById("truckNum");
var source = document.getElementById("source");
var shiftDate = document.getElementById("shiftDate");
var startTime = document.getElementById("startTime");
var endTime = document.getElementById("endTime");
var logSheet = document.getElementById("logSheet");
var drivers = "{{drivers}}"

function checkData() {
    var driverIdValue = driverId.value.trim();
    var clientIdValue = clientId.value.trim();
    var shiftTypeValue = shiftType.value.trim();
    var numberOfLogsValue = numberOfLogs.value.trim();
    var truckNumValue = truckNum.value.trim();
    var sourceValue = source.value.trim();
    var shiftDateValue = shiftDate.value.trim();
    var startTimeValue = startTime.value.trim();
    var endTimeValue = endTime.value.trim();
    var logSheetValue = logSheet.value.trim();

    var isValid = true;



    if (drivers) {
        if (driverIdValue == "") {
            setError(driverId, "Driver id can't be left blank.");
            $("#driverId").next('.dselect-wrapper').addClass('isInvalid')
            isValid = false;
        } else {
            setSuccess(driverId);
        }
    } else {
        if (driverIdValue == "") {
            setError(driverId, "Driver ID can't be blank.");
            $("#driverId").addClass('isInvalid')
            isValid = false;
        } else {
            setSuccess(driverId);
        }
    }

    if (clientIdValue == "") {
        setError(clientId, "Client ID can't be blank.");
        $("#clientId").next('.dselect-wrapper').addClass('isInvalid')

        isValid = false;
    } else {
        setSuccess(clientId);
    }
    if (shiftTypeValue == "") {
        setError(shiftType, "Shift type can't be empty.");
        isValid = false;
    } else {
        setSuccess(shiftType);
    }
    if (numberOfLogsValue == "") {
        setError(numberOfLogs, "Number of loads can't be empty.");
        isValid = false;
    } else {
        setSuccess(numberOfLogs);
    }
    if (truckNumValue == "") {
        setError(truckNum, "Truck number can't be left blank.");
        $("#truckNum").next('.dselect-wrapper').addClass('isInvalid')

        isValid = false;
    } else {
        setSuccess(truckNum);
    }

    if (shiftDateValue == "") {
        setError(shiftDate, "Shift date can't be blank.");
        isValid = false;
    } else {
        setSuccess(shiftDate);
    }

    if (sourceValue == "") {
        setError(source, "source can't be left blank.");
        $("#source").next('.dselect-wrapper').addClass('isInvalid')

        isValid = false;
    } else {
        setSuccess(source);
    }

    if (startTimeValue == "") {
        setError(startTime, "Start time can't be blank.");
        isValid = false;
    } else {
        setSuccess(startTime);
    }
    if (endTimeValue == "") {
        setError(endTime, "End time can't be blank.");
        isValid = false;
    } else {
        setSuccess(endTime);
    }

    if (logSheetValue == "") {
        setError(logSheet, "Please upload a Load Sheet.");
        isValid = false;
    } else {
        setSuccess(logSheet);
    }

    var invalidInputs = document.querySelectorAll('.isInvalid');
    invalidInputs.forEach(function (input) {
        setError(input, "This field is required.");
    });

    return isValid;
}

function setError(inputElement, msg) {
    var parentBox = inputElement.parentElement;
    parentBox.classList.remove("success");
    parentBox.classList.add("error");
    var span = parentBox.querySelector(".errorMsg");
    var fa = parentBox.querySelector(".fa");
    span.innerText = msg;
    fa.className = "fa fa-exclamation-circle";
    inputElement.style.borderColor = "rgb(255, 0, 0)";
}

function setSuccess(inputElement) {
    var parentBox = inputElement.parentElement;
    parentBox.classList.remove("error");
    parentBox.classList.add("success");
    var span = parentBox.querySelector(".errorMsg");
    span.innerText = "";
    var fa = parentBox.querySelector(".fa");
    $(`#${inputElement.id}`).next('.dselect-wrapper').removeClass('isInvalid')
    fa.className = "fa fa-check-circle";
    inputElement.style.borderColor = "";
}

var select_box_element = document.querySelector("#clientId");

dselect(select_box_element, {
    search: true,
});

var select_box_element = document.querySelector("#source");

dselect(select_box_element, {
    search: true,
});

var select_box_element = document.querySelector("#truckNum");

dselect(select_box_element, {
    search: true,
});

if (drivers) {
    var driverIdSelect = document.querySelector("#driverId");

    dselect(driverIdSelect, {
        search: true,
    });
}

// Get the input element
const numberOfLogsInput = document.getElementById('numberOfLogs');

// Add an event listener for input changes
numberOfLogsInput.addEventListener('input', function () {
    // Remove leading zeros
    this.value = this.value.replace(/^1+/, '');

    // Convert to positive integer
    let value = parseInt(this.value) || 1;

    // Update the input value
    this.value = value;
});


// get truck number  using client name
$("#clientId").on('change', function () {
    // var searchableDropdown = $('#truckNum');
    // var searchInput = $('#searchInput');

    // function populateDropdown(data) {
    //     searchableDropdown.empty();
    //     searchableDropdown.append($('<option>', {
    //         value: null,
    //         text: null,
    //         selected: true,
    //         disabled: true
    //     }));
    //     $.each(data, function (index, option) {
    //         searchableDropdown.append($('<option>', {
    //             value: option,
    //             text: option
    //         }));
    //     });
    // }
    // function filterOptions() {
    //     var searchText = searchInput.val().toLowerCase();
    //     searchableDropdown.find('option').each(function () {
    //         var optionText = $(this).text().toLowerCase();
    //         $(this).toggle(optionText.indexOf(searchText) > -1);
    //     });
    // }

    $.ajax({
        type: "POST",
        // url: "{% url 'DriverSchedule_app:downloadAnalysis' %}", // Replace with the actual URL
        url: "/DriverSchedule_app/getTrucks/", // Replace with the actual URL
        data: {
            clientName: $(this).val()
        },
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (data) {
            var selectOptions = $('#truckNum');
            // populateDropdown(data.trucks)
            var options = ''

            $.each(data.trucks, function (index, option) {
                options += `<button class="dropdown-item" data-dselect-value="${option}" type="button" onclick="dselectUpdate(this, 'dselect-wrapper', 'form-select')">${option}</button>`
            });

            let append_data =
                `<div class="dropdown dselect-wrapper ">
                    <button class="form-select" data-dselect-text="" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                        <span class="dselect-placeholder">Select Truck No</span>
                    </button>
                    <div class="dropdown-menu" style="">
                        <div class="d-flex flex-column">
                            <input onkeydown="return event.key !== 'Enter'" onkeyup="dselectSearch(event, this, 'dselect-wrapper', 'form-select', false)" type="text" class="form-control" placeholder="Search" autofocus="">
                            <div class="dselect-items" style="max-height:360px;overflow:auto">
                                <button hidden="" class="dropdown-item active" data-dselect-value="" type="button" onclick="dselectUpdate(this, 'dselect-wrapper', 'form-select')">Select Truck No</button>
                                ${options}
                            </div>
                            <div class="dselect-no-results d-none">No results found</div>
                        </div>
                    </div>            
                </div>`
            $("#truckNum").next('.dselect-placeholder').remove();
            $("#truckNum").after(append_data);

            console.log(data.trucks); // Process the data received from the server
        },
    });
    // searchInput.on('input', function () {
    //     filterOptions();
    // });
});
