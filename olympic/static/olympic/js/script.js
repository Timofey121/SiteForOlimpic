$(function() {
	$(".icon_menu").click(function() {
	$(".nav").toggleClass("nav_active");
    $(".nav_mobile").toggleClass("nav_mobile_active");
    $(".connect_container").removeClass("connect_container_active");
	});
});
$(function() {
	$(".accout_svg_disactive").click(function() {
	$(".connect_container").toggleClass("connect_container_active");
	});
});

$('body').on('click', '.icon_hide', function(){
	if ($('#password_input').attr('type') == 'password'){
		$(this).addClass('view');
		$('#password_input').attr('type', 'text');
	} else {
		$(this).removeClass('view');
		$('#password_input').attr('type', 'password');
	}
	return false;
});


