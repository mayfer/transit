$(document).ready(function() {
	$('.default-value').each(function() {
		var default_value = this.value;
		var prompt_value = $(this).attr('title');
		if(!default_value) {
			this.value = prompt_value;
			$(this).addClass('waiting-for-input');
		}
		$(this).focus(function() {
			if(this.value == prompt_value) {
				$(this).removeClass('waiting-for-input');
				this.value = '';
			}
		});
		$(this).blur(function() {
			if(this.value == '') {
				$(this).addClass('waiting-for-input');
				this.value = prompt_value;
			}
		});
	});
});

function remove_leading_zeros(string) {
    return string.replace(/^[0]*/g, '');
}