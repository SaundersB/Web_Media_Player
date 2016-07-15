var screen_height = window.innerHeight;
var screen_width = window.innerWidth;

console.log(screen_height);
console.log(screen_width);


function animateByIdFadeIn(currentDiv, nextDiv) {
	console.log("animateByIdFadeIn");
	TweenMax.fromTo(document.getElementById(currentDiv), 1, {opacity: 1}, {opacity: 0});
}

function completeHandler() {
	console.log("Done");
}


function scroll_text_right(text){
	console.log("scrolling_text");
	TweenMax.to(text, 50, {x:screen_width, yoyo:true, repeat:-1 });
	//TweenMax.to(text, 10, {scrollX:100, repeat:5, ease:Linear.easeNone});
}

function scroll_text_left(text){
	console.log("scrolling_text");
	TweenMax.to(text, 50, {x:-screen_width, yoyo:true, repeat:-1 });
	//TweenMax.to(text, 10, {scrollX:100, repeat:5, ease:Linear.easeNone});
}

function shift_text(text){
	console.log("scroll_text");
	TweenMax.to(text, 10, {x:100, y:200});
	//TweenMax.to(text, 10, {scrollX:100, repeat:5, ease:Linear.easeNone});
}

var starting_div = document.getElementById("scrolling_text");
var ending_div = document.getElementById("additional_text");



scroll_text_right(starting_div);
scroll_text_left(ending_div);
