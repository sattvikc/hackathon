'use strict';

function InputPort(options) {
  var self = this;
  self.name = options.name;
  self.value = options.value;
  self.taskNode = options.taskNode;
  self.task = options.task;
  self.xOffset = options.xOffset;
  self.yOffset = options.yOffset;

  self.init = function() {
    self.taskNode.append('circle')
      .attr('class', 'task-node__inputport')
      .attr('cx', self.xOffset)
      .attr('cy', self.yOffset)
      .attr('r', self.task.ui.port_radius);
  }

  self.coordinates = function() {
    return {
      'x': (self.task.ui.x + self.xOffset),
      'y': (self.task.ui.y + self.yOffset)
    };
  }

  self.init();
}

function OutputPort(options) {
  var self = this;
  self.name = options.name;
  self.taskNode = options.taskNode;
  self.task = options.task;
  self.xOffset = options.xOffset;
  self.yOffset = options.yOffset;

  self.init = function() {
    self.taskNode.append('circle')
      .attr('class', 'task-node__outputport')
      .attr('cx', self.xOffset)
      .attr('cy', self.yOffset)
      .attr('r', self.task.ui.port_radius);
  }

  self.coordinates = function() {
    return {
      'x': (self.task.ui.x + self.xOffset),
      'y': (self.task.ui.y + self.yOffset)
    };
  }

  self.init();
}


function TaskNode(viewport, svg, task) {
  var self = this;
  self.viewport = viewport;
  self.svg = svg;
  self.task = task;
  self.taskNode = false;
  self.inputPorts = [];
  self.outputPorts = [];

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
        self.viewport.renderConnectors();
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

  self.renderTaskNode = function() {
    if(self.taskNode) {
      self.taskNode.remove();
    }
    self.taskNode = self.svg.append('g');
    self.taskNode.call(self.handleDragDrop());
    self.taskNode.attr('transform', 'translate(' + [task.ui.x, task.ui.y] + ')');
    self.taskNode.append('foreignObject')
      .html($('#tmpl-task-node').tmpl({'task': task}).html())
      .attr('width', task.ui.width)
      .attr('height', task.ui.height);
  }

  self.renderInputPorts = function() {
    self.inputPorts = [];
    var xOffset = 0;
    var yOffset = (-task.ui.port_radius/2);
    var index = 0;
    if(!('inputs' in task)) {
      return
    }
    for(var name in task.inputs) {
      var value = task.inputs[name];
      xOffset += task.ui.port_spacing;
      self.inputPorts.push(new InputPort({
        'name': name,
        'value': value,
        'taskNode': self.taskNode,
        'task': self.task,
        'xOffset': xOffset,
        'yOffset': yOffset
      }));
    }
  }

  self.renderOutputPorts = function() {
    self.outputPorts = [];
    var xOffset = task.ui.width;
    var yOffset = (task.ui.height + task.ui.port_radius/2);
    if(!('outputs' in task)) {
      return
    }
    for(var i=0; i<task.outputs.length; i++) {
      var name = task.outputs[i];
      xOffset -= task.ui.port_spacing;
      self.outputPorts.push(new OutputPort({
        'name': name,
        'taskNode': self.taskNode,
        'task': self.task,
        'xOffset': xOffset,
        'yOffset': yOffset
      }));
    }
  }

  self.render = function() {
    self.renderTaskNode();
    self.renderInputPorts();
    self.renderOutputPorts();
  }

  self.init = function() {
    self.render();
  }

  self.init();
}

function WorkflowViewPort(identifier) {
  var self = this;
  self.taskNodes = [];
  self.connectors = [];
  self.connectorPaths = [];

  self.addTaskItem = function(task) {
    var taskNode = new TaskNode(self, self.svg, task);
    self.taskNodes.push(taskNode);
  }

  self.addTasks = function(tasks) {
    for(var i=0; i<tasks.length; i++) {
      self.addTaskItem(tasks[i]);
    }
  }

  self.getTaskNodeByName = function(name) {
    for(var i=0; i<self.taskNodes.length; i++) {
      var taskNode = self.taskNodes[i];
      if(taskNode.task.name == name) {
        return taskNode;
      }
    }
  }

  self.getOutputPortByKey = function(key) {
    var taskName = key.split('.')[0];
    var portName = key.split('.')[1];
    var taskNode = self.getTaskNodeByName(taskName);
    for(var i=0; i<taskNode.outputPorts.length; i++) {
      if(portName == taskNode.outputPorts[i].name) {
        return taskNode.outputPorts[i];
      }
    }
  }

  self.loadConnectors = function() {
    self.connectors = [];
    for(var i=0; i<self.taskNodes.length; i++) {
      var taskNode = self.taskNodes[i];
      if(!('inputs' in taskNode.task)) {
        continue;
      }
      for(var j=0; j<taskNode.inputPorts.length; j++) {
        var inputPort = taskNode.inputPorts[j];
        if(inputPort.value.src == 'taskout') {
          var key = inputPort.value.key;
          var outputPort = self.getOutputPortByKey(key);
          self.connectors.push({
            'inputPort': inputPort,
            'outputPort': outputPort
          });
        }
      }
    }
  }

  self.renderConnector = function(p1, p2) {
    var lineFunction = d3.svg.line()
      .x(function(d) { return d.x; })
      .y(function(d) { return d.y; })
      .interpolate("linear");
    var lineData = [];
    lineData.push(p1);
    lineData.push({x: p1.x+15, y: p1.y+15});
    lineData.push({x: (p1.x+p2.x)/2, y: p1.y+15});
    lineData.push({x: (p1.x+p2.x)/2, y: p2.y-15});
    lineData.push({x: p2.x-15, y: p2.y-15});
    lineData.push(p2);

    var path = self.svg.append('path')
      .attr('d', lineFunction(lineData))
      .attr('class', 'task-node-connector');
    self.connectorPaths.push(path);
  }

  self.renderConnectors = function() {
    for(var i=0; i<self.connectorPaths.length; i++) {
      self.connectorPaths[i].remove();
    }
    self.loadConnectors();
    for(var i=0; i<self.connectors.length; i++) {
      var connector = self.connectors[i];
      var startX = connector.outputPort.coordinates().x;
      var startY = connector.outputPort.coordinates().y;
      var endX = connector.inputPort.coordinates().x;
      var endY = connector.inputPort.coordinates().y;
      self.renderConnector({'x': startX, 'y': startY}, {'x': endX, 'y': endY});
    }
  }

  self.init = function() {
    self.svg = d3.select(identifier)
      .append('svg')
      .attr('width', '100%')
      .attr('height', '100%');
  }

  self.init();
}
