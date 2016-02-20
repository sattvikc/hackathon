'use strict';


function TaskNode(viewport, svg, task) {
  var self = this;
  self.viewport = viewport;
  self.svg = svg;
  self.task = task;
  self.taskNode = false;

  self.handleDragDrop = function() {
    var drag = d3.behavior.drag()
      .origin(function() { 
        var t = d3.select(this);
        return {
          x: t.attr('x') + d3.transform(t.attr('transform')).translate[0],
          y: t.attr('y') + d3.transform(t.attr('transform')).translate[1]
        };
      })
      .on('dragstart', function() {
        d3.event.sourceEvent.stopPropagation();
      })
      .on('drag', function(d, i) {
        self.task.ui.x = d3.event.x;
        self.task.ui.y = d3.event.y;
        d3.select(this).attr('transform', 'translate(' + [d3.event.x, d3.event.y] + ')');
      })
      .on('dragend', function() {
        for(var i=0; i<self.viewport.taskNodes.length; i++) {
          self.viewport.taskNodes[i].task.ui.selected = false
          self.viewport.taskNodes[i].render();
        }
        self.task.ui.selected = true;
        self.render();
      });
    return drag;
  }

  self.render = function() {
    if(self.taskNode) {
      self.taskNode.remove();
    }
    self.taskNode = self.svg.append('g');
    self.taskNode.call(self.handleDragDrop());
    var taskNodeContent = $('#tmpl-task-node').html();
    self.taskNode.append('foreignObject')
      .html($('#tmpl-task-node').tmpl({'task': task}).html())
      .attr('width', task.ui.width)
      .attr('height', task.ui.height);
    self.taskNode.attr('transform', 'translate(' + [task.ui.x, task.ui.y] + ')');
  }

  self.init = function() {
    self.render();
  }

  self.init();
}

function WorkflowViewPort(identifier) {
  var self = this;
  self.taskNodes = [];

  self.addTaskItem = function(task) {
    var taskNode = new TaskNode(self, self.svg, task);
    self.taskNodes.push(taskNode);
  }

  self.init = function() {
    self.svg = d3.select(identifier)
      .append('svg')
      .attr('width', '100%')
      .attr('height', '100%');
  }

  self.init();
}
