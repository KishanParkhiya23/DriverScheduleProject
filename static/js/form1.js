const csrftoken = $("[name=csrfmiddlewaretoken]").val();

if ($(window).width() < 1000) {
  $("body #mainCont").addClass("container-fluid");
  $("body #mainCont").removeClass("container");
} else {
}

document.getElementById("nextBtn").addEventListener("click", function (event) {
  event.preventDefault();

  if (checkData()) {
    let truckNumElement = document.getElementById("truckNum");
    let selectedValue =
      truckNumElement.options[truckNumElement.selectedIndex].text;

    $("select[name='truckNum']").val(selectedValue);
    $("#signUpForm").submit();
  }
});

var driverId = document.getElementById("driverId");
var clientId = document.getElementById("clientId");
var shiftType = document.getElementById("shiftType");
var numberOfLoads = document.getElementById("numberOfLoads");
var truckNum = document.getElementById("truckNum");
var source = document.getElementById("source");
var shiftDate = document.getElementById("shiftDate");
var startTime = document.getElementById("startTime");
var endTime = document.getElementById("endTime");
var logSheet = document.getElementById("logSheet");
var drivers = "{{drivers}}";

function checkData() {
  var driverIdValue = driverId.value.trim();
  var clientIdValue = clientId.value.trim();
  var shiftTypeValue = shiftType.value.trim();
  var numberOfLoadsValue = numberOfLoads.value.trim();
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
      $("#driverId").next(".dselect-wrapper").addClass("isInvalid");
      isValid = false;
    } else {
      setSuccess(driverId);
    }
  } else {
    if (driverIdValue == "") {
      setError(driverId, "Driver ID can't be blank.");
      $("#driverId").addClass("isInvalid");
      isValid = false;
    } else {
      setSuccess(driverId);
    }
  }

  if (clientIdValue == "") {
    setError(clientId, "Client ID can't be blank.");
    $("#clientId").next(".dselect-wrapper").addClass("isInvalid");

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
  if (numberOfLoadsValue == "") {
    setError(numberOfLoads, "Number of loads can't be empty.");
    isValid = false;
  } else {
    setSuccess(numberOfLoads);
  }
  if (truckNumValue == "") {
    setError(truckNum, "Truck number can't be left blank.");
    $(".select2-selection").eq(0).addClass("isInvalid");
    isValid = false;
  } else {
    setSuccess(truckNum);
    $(".select2-selection").eq(0).removeClass("isInvalid");
  }

  if (shiftDateValue == "") {
    setError(shiftDate, "Shift date can't be blank.");
    isValid = false;
  } else {
    setSuccess(shiftDate);
  }

  if (sourceValue == "") {
    setError(source, "source can't be left blank.");
    $("#source").next(".dselect-wrapper").addClass("isInvalid");

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

  var invalidInputs = document.querySelectorAll(".isInvalid");
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
  $(`#${inputElement.id}`).next(".dselect-wrapper").removeClass("isInvalid");
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

if (drivers) {
  var driverIdSelect = document.querySelector("#driverId");

  dselect(driverIdSelect, {
    search: true,
  });
}

// Get the input element
const numberOfLoadsInput = document.getElementById("numberOfLoads");

// Add an event listener for input changes
numberOfLoadsInput.addEventListener("input", function () {
  // Remove leading zeros
  this.value = this.value.replace(/^1+/, "");

  // Convert to positive integer
  let value = parseInt(this.value) || 1;

  // Update the input value
  this.value = value;
});

$(".js-select2").select2({
  width: "100%",
});

// get truck number  using client name
$(".select2-selection").eq(1).hide();

$("#clientId").on("change", function () {
  let clientId = $(this).val();

  if (clientId) {
    $("#truckNum").prop("disabled", false);
    $("#truckNum").html('<option value="">Loading...</option>');
    $.ajax({
      type: "POST",
      url: "/DriverSchedule_app/getTrucks/",
      data: {
        clientName: $(this).val(),
      },
      beforeSend: function (xhr) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      },
      success: function (data) {
        $("#truckNum").html('<option value="">Select an Item</option>');
        // console.log(data.trucks);
        data.trucks.forEach(function (item) {
          //   console.log(item);
          $("#truckNum").append(
            '<option value="' + item + '">' + item + "</option>"
          );
        });
        $("#truckNum").trigger("change.select2");
      },
    });
  }
});
