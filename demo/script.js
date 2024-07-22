// Set the server host and port. You can change these parameters as needed.
const serverHost = 'localhost';
const serverPort = 7712;

$(document).ready(function() {
    $('.tab-button').click(function() {
        $('.tab-button').removeClass('active');
        $(this).addClass('active');
        $('.tab-content').hide();
        $('#' + $(this).attr('data-target')).show();
    });

   // Set default active tab
   $('#datarefs').show();
   $('.tab-button[data-target="datarefs"]').addClass('active');

    // Update the FastAPI documentation link dynamically
    var docsUrl = `http://${serverHost}:${serverPort}/docs`;
    $('a[href$="/docs"]').attr('href', docsUrl).text(docsUrl);

   $('#commands-form').submit(function(event) {
       event.preventDefault();
       sendCommand($('#command').val());
   });

   $('#datarefs-form').submit(function(event) {
       event.preventDefault();
       getDataref($('#dataref').val().split(',').map(d => d.trim()));
   });

   $('#set-datarefs-form').submit(function(event) {
       event.preventDefault();
       var datarefs = $('#set-dataref').val().split(',').map(d => d.trim());
       var values = $('#set-value').val().split(',').map(v => v.trim());
       setDataref(datarefs, values);
   });

    $('.toggle-json').click(function(event) {
        event.preventDefault();
        let target = $(this).closest('.tab-content').find('.output');
        target.html(target.data('raw'));
    });

    $('.toggle-formatted').click(function(event) {
        event.preventDefault();
        let target = $(this).closest('.tab-content').find('.output');
        target.html(target.data('formatted'));
    });
});

function sendCommand(command) {
    $.ajax({
        url: `http://${serverHost}:${serverPort}/command`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ command }),
        success: function(response) {
            let resultBox = $('#commands-result');
            resultBox.html(`<pre>Successfully Triggered: ${JSON.stringify(response, null, 2)}</pre>`);
            resultBox.show();
        },
        error: function(xhr) {
            let resultBox = $('#commands-result');
            resultBox.html(`<pre>Error: ${xhr.responseText}</pre>`);
            resultBox.show();
        }
    });
}

function getDataref(datarefs) {
    $.ajax({
        url: `http://${serverHost}:${serverPort}/get_dataref`,
        method: 'GET',
        data: { datarefs: datarefs.join(',') },
        success: function(response) {
            let resultBox = $('#read-datarefs-result');
            let raw = JSON.stringify(response, null, 2);
            let formatted = response.map(d => `<strong>${d.dataref}</strong>: ${d.value}`).join('<br>');
            resultBox.data('raw', raw).data('formatted', formatted).html(formatted);
            resultBox.show();
            $('#read-datarefs-toggle').show();
        },
        error: function(xhr) {
            let resultBox = $('#read-datarefs-result');
            resultBox.html(`<pre>Error: ${xhr.responseText}</pre>`);
            resultBox.show();
        }
    });
}

function setDataref(datarefs, values) {
    if(datarefs.length !== values.length) {
        alert("The number of datarefs and values must match.");
        return;
    }
    
    let requestData;
    // Check if there is only one dataref and one value or multiple
    if (datarefs.length === 1) {
        requestData = {
            dataref: datarefs[0],
            value: values[0]
        };
    } else {
        requestData = {
            dataref: datarefs,
            value: values
        };
    }
    
    $.ajax({
        url: `http://${serverHost}:${serverPort}/set_dataref`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(requestData),
        success: function(response) {
            let resultBox = $('#write-datarefs-result');
            let raw = JSON.stringify(response, null, 2);
            let formatted = `Successfully Updated: ${datarefs.map((d, i) => `${d} to ${values[i]}`).join(', ')}`;
            resultBox.data('raw', raw).data('formatted', formatted).html(formatted);
            resultBox.show();
            $('#write-datarefs-toggle').show();
        },
        error: function(xhr) {
            let resultBox = $('#write-datarefs-result');
            resultBox.html(`<pre>Error: ${JSON.stringify(JSON.parse(xhr.responseText), null, 2)}</pre>`);
            resultBox.show();
        }
    });
}

