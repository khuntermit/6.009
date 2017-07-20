"use strict";

// RPC wrapper
function invoke_rpc(method, args, timeout, on_done){
  $("#crash").hide();
  $("#timeout").hide();
  $("#rpc_spinner").show();
  //send RPC with whatever data is appropriate. Display an error message on crash or timeout
  var xhr = new XMLHttpRequest();
  xhr.open("POST", method, true);
  xhr.setRequestHeader('Content-Type','application/json; charset=UTF-8');
  xhr.timeout = timeout;
  xhr.send(JSON.stringify(args));
  xhr.ontimeout = function () {
    $("#timeout").show();
    $("#rpc_spinner").hide();
    $("#crash").hide();
  };
  xhr.onloadend = function() {
    if (xhr.status === 200) {
      $("#rpc_spinner").hide();
      var result = JSON.parse(xhr.responseText)
      $("#timeout").hide();
      if (typeof(on_done) != "undefined"){
        on_done(result);
      }
    } else {
      $("#crash").show();
    }
  }
}

// Resource load wrapper
function load_resource(name, on_done) {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", name, true);
  xhr.onloadend = function() {
    if (xhr.status === 200) {
      var result = JSON.parse(xhr.responseText);
      on_done(result);
    }
  }
  xhr.send();
}

// Code that runs first
$(document).ready(function(){
    // race condition if init() does RPC on function not yet registered by restart()!
    //restart();
    //init();
    invoke_rpc( "/restart", {}, 0, function() { init(); } )
});

function restart(){
  invoke_rpc( "/restart", {} )
}

//  LAB CODE

// this is inlined into infra/ui/ui.js

// State
var test_cases = {};
var current_test_case = null;

// matrix accessors
function get_element(maze, r, c) {
  return maze.maze[r][c];
}

function is_valid(solution, r, c) {
  var valid = true;

  // is x,y inside the maze?
  valid &= ((r>=0) && (r<solution.dimensions[0]));
  valid &= ((c>=0) && (c<solution.dimensions[1]));

  // is there a path from r,c to the solution?

  if (valid) {
    valid &= (get_element(solution, r, c) != "X");
  }

  return valid;
}

// Convert value matrix to one path
function find_max_path(solution, start,  goal) {
  var path = [];

  if (get_element(solution, goal[0], goal[1]) != "X") {

    var r = goal[0];
    var c = goal[1];

    while ((r != start[0]) || (c != start[1])) {
      path.push([r,c]);

      // is there a valid path to the left?
      var left_valid = is_valid(solution, r, c-1);
      var up_valid = is_valid(solution, r-1, c);
      if (left_valid && up_valid) {
        var left = get_element(solution, r, c-1);
        var up = get_element(solution, r-1, c);
        if (left > up) {
          c = c-1;
        } else {
          r = r-1;
        }
      } else if (left_valid) {
        c = c-1;
      } else if (up_valid) {
        r = r-1;
      } else {
        return []; // this solution is crazy wrong
      }
    }

    path.push([start[0],start[1]]);
    path.reverse();
  }
  return path;
}

// Render logic
function render(state, solution) {
  clear_primitives();

  if (state == null) return;

  draw.viewbox(0, 0, state.m.dimensions[1], state.m.dimensions[0]);
  draw.height = draw.width*state.m.dimensions[0]/state.m.dimensions[1];

  // Draw grid
  for (var c=0; c<=state.m.dimensions[1]; c++){
    draw_line(c,0, c,state.m.dimensions[0]).stroke({ width: 0.025, color: '#000' });
  }

  for (var r=0; r<=state.m.dimensions[0]; r++){
    draw_line(0,r, state.m.dimensions[1],r).stroke({ width: 0.025, color: '#000' });
  }

  // Draw start and goal
  draw_rect().move(state.start[1], state.start[0]).size(1,1).fill({color: '#03A9F4', opacity: 0.5 });
  draw_rect().move(state.goal[1], state.goal[0]).size(1,1).fill({color: '#03A9F4', opacity: 0.5 });

  var path = [];

  // Draw result if it is available
  if (solution != null) {
    // Find the max value
    var max_value = 0;
    for (var c=0; c<state.m.dimensions[1]; c++){
      for (var r=0; r<state.m.dimensions[0]; r++){
        var cell = get_element(solution, r, c);
        if (cell != "X") max_value = Math.max(max_value, cell);
      }
    }

    // Draw overlay
    for (var c=0; c<state.m.dimensions[1]; c++){
      for (var r=0; r<state.m.dimensions[0]; r++){
        var cell = get_element(solution, r, c);
        if (cell == "X") {
          draw_rect().move(c+0.1,r+0.1).size(0.8,0.8).fill({color: '#E91E63', opacity: 0.5 });
        } else {
          var value = (cell / max_value)*0.75;
          draw_rect().move(c+0.1,r+0.1).size(0.8,0.8).fill({color: '#4CAF50', opacity: value });
        }
      }
    }

    // Draw path
    path = find_max_path(solution, state.start, state.goal);
    for (var i=1; i<path.length; i++) {
      draw_line(path[i-1][1]+0.5,path[i-1][0]+0.5, path[i][1]+0.5,path[i][0]+0.5).stroke({ width: 0.1, color: '#03A9F4', opacity: 1 });
    }
  }

  // Place grid items
    for (var c=0; c<state.m.dimensions[1]; c++){
      for (var r=0; r<state.m.dimensions[0]; r++){
      var cell = get_element(state.m, r, c);
      if (cell == 1) { // wall
        draw_rect().move(c,r).size(1,1).fill({color: '#000', opacity: 0.5 });
      } else if (cell == "c") { // coin
        draw_image("coin").move(c+0.1,r+0.1).size(0.8,0.8);
      } else if (cell == "b") { // bomb
        draw_image("bomb").move(c+0.1,r+0.1).size(0.8,0.8);
      }
    }
  }

  // Draw path
  for (var i=1; i<path.length; i++) {
    draw_line(path[i-1][1]+0.5,path[i-1][0]+0.5, path[i][1]+0.5,path[i][0]+0.5).stroke({ width: 0.1, color: '#03A9F4', opacity: 1 });
  }

  // Hide remaining cached primitives
  render_primitives();
}

// Render back-end library
var draw;
var rectangle_cache = [];
var rectangle_counter = 0;
var line_cache = [];
var line_counter = 0;
var image_cache = [];

function clear_primitives() {
  rectangle_counter = 0;
  line_counter = 0;

  for (var i in image_cache) {
    image_cache[i].remove();
  }
}

function render_primitives() {
  while (rectangle_counter < rectangle_cache.length) {
    rectangle_cache[rectangle_counter].hide();
    rectangle_counter++;
  }
  while (line_counter < line_cache.length) {
    line_cache[line_counter].hide();
    line_counter++;
  }
}

function draw_rect() {
  if (rectangle_cache.length < (rectangle_counter+1)) {
    rectangle_cache.push(draw.rect(1,1));
  }
  rectangle_counter ++;
  var r = rectangle_cache[rectangle_counter-1];
  r.show();
  return r;
}

function draw_image(image) {
  var i = draw.image("/resources/"+image+".svg", 100, 100);
  image_cache.push(i);
  return i;
}

function draw_line(x0, y0, x1, y1) {
  if (line_cache.length < (line_counter+1)) {
    line_cache.push(draw.line(0,0,1,1));
  }
  line_counter ++;
  var l = line_cache[line_counter-1];
  l.plot(x0,y0, x1,y1);
  l.show();
  return l;
}

// UI button handlers
function handle_select(test_case_name) {
  // test case is already loaded in memory, simply switch to it!
  $("#current_test").html(test_case_name);
  current_test_case = test_cases[test_case_name].inputs;
  render(current_test_case, null);
}

function handle_solve() {
  // RPC to server.py to
  var solve_callback = function( solution ) {
    // print cost of best path
    var coins = get_element(solution, current_test_case.goal[0], current_test_case.goal[1]);
    if (coins == "X") {
      $("#best_coins").html("Your code found no path.");
    } else {
      $("#best_coins").html("Your code suggests the best path collects " + coins + " coins!");
    }

    // Render the solution
    render(current_test_case, solution);
  };
  invoke_rpc("/run_test", { function: "solve_maze", inputs: current_test_case }, 5000, solve_callback);
}

// Initialization code (called when the UI is loaded)
function init() {
  draw = SVG('drawing');
  SVG.on(window, 'resize', function() { draw.spof() });

  // Load list of test cases
  var test_case_names_callback = function( test_cases_names ) {
    for (var i in test_cases_names) {
      if (i == 13) continue; // Make sure don't add the huge maze
      var filename = test_cases_names[i];
      if (!(filename.match(/.*?[.]in/i))) continue;

      var test_case_callback = function( test_case ) {
        var first = Object.keys(test_cases).length == 0;
        var test_case_name = test_case.test;
        test_cases[test_case_name] = test_case;

        $("#test_cases").append(
          "<li class=\"mdl-menu__item\" onclick=\"handle_select('" +
          test_case_name +
          "')\">" +
          test_case_name +
          "</li>");

        // is it first? select it!
        if (first) handle_select(test_case.test);
      };
      invoke_rpc("/load_json", { "path": "cases/"+filename }, 0, test_case_callback);
    };
  };
  invoke_rpc("/ls", { "path": "cases/" }, 0, test_case_names_callback);
}


