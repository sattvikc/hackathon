'use strict';

function getEmptyTask(svg) {
  return {
    "inputs": [],
    "outputs": [],
    "dependencies": [],
    "ui": {
      "x": 10,
      "y": 10,
      "width": 250,
      "height": 80,
      "selected": false,
      "port_radius": 4,
      "port_hover_radius": 6,
      "port_spacing": 20
    }
  };
}

function InputPort(options) {
  var self = this;
  self.name = options.name;
  self.src = options.src;
  self.key = options.key;
  self.svg = options.svg;
  self.viewport = options.viewport;
  self.taskNode = options.taskNode;
  self.taskObj = options.taskObj;
  self.task = options.task;
  self.xOffset = options.xOffset;
  self.yOffset = options.yOffset;

  self.handleMouseOver = function() {
    self.circle.attr('r', self.task.ui.port_hover_radius);
  }

  self.handleMouseOut = function() {
    self.circle.attr('r', self.task.ui.port_radius);
  }

  self.handleDragDrop = function() {
    var drag = d3.behavior.drag()
      .on('dragstart', function() {
        d3.event.sourceEvent.stopPropagation();
      })
      .on('drag', function(d, i) {
        d3.event.sourceEvent.stopPropagation();
      })
      .on('dragend', function() {
        //d3.event.sourceEvent.stopPropagation();
      });
    return drag;
  }

  self.handleDoubleClick = function() {
    for(var i=0; i<self.task.inputs.length; i++) {
      var input = self.task.inputs[i];
      if(input.name == self.name) {
        self.task.inputs[i] = {'name': self.name, 'src': '', 'key': ''};
      }
    }
    self.taskObj.render();
    self.viewport.renderConnectors();
  }

  self.init = function() {
    self.circle = self.taskNode.append('circle')
      .attr('class', 'task-node__inputport')
      .attr('cx', self.xOffset)
      .attr('cy', self.yOffset)
      .attr('r', self.task.ui.port_radius)
      .on('mouseover', self.handleMouseOver)
      .on('mouseout', self.handleMouseOut)
      .call(self.handleDragDrop())
      .on('click', self.handleDoubleClick);
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
  self.svg = options.svg;
  self.viewport = options.viewport;
  self.taskNode = options.taskNode;
  self.taskObj = options.taskObj;
  self.task = options.task;
  self.xOffset = options.xOffset;
  self.yOffset = options.yOffset;
  self.index = options.index;
  self.tempConnector = false;
  self.tempInputPort = false;

  self.handleMouseOver = function() {
    self.circle.attr('r', self.task.ui.port_hover_radius);
  }

  self.handleMouseOut = function() {
    self.circle.attr('r', self.task.ui.port_radius);
  }

  self.handleDragDrop = function() {
    var drag = d3.behavior.drag()
      .on('dragstart', function() {
        d3.event.sourceEvent.stopPropagation();
      })
      .on('drag', function(d, i) {
        if(self.tempConnector) {
          self.tempConnector.remove();
        }
        var mouse = {
          'x': self.task.ui.x + d3.event.x,
          'y': self.task.ui.y + d3.event.y
        }
        var response = self.viewport.findNearestInputPort(mouse);
        if(response.found) {
          self.tempConnector = self.viewport.renderPath(
            self.coordinates(), response.inputPort.coordinates(), self.index);
          self.tempInputPort = response.inputPort;
        }
        else {
          self.tempConnector = self.viewport.renderPath(
            self.coordinates(), mouse, self.index);
          self.tempInputPort = response.inputPort;
        }
      })
      .on('dragend', function() {
        if(self.tempInputPort) {
          self.viewport.addConnector(self, self.tempInputPort);
        }
        self.tempInputPort = false;
        if(self.tempConnector) {
          self.tempConnector.remove();
        }
      });
    return drag;
  }

  self.init = function() {
    self.circle = self.taskNode.append('circle')
      .attr('class', 'task-node__outputport')
      .attr('cx', self.xOffset)
      .attr('cy', self.yOffset)
      .attr('r', self.task.ui.port_radius)
      .call(self.handleDragDrop())
      .on('mouseover', self.handleMouseOver)
      .on('mouseout', self.handleMouseOut);
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
  self.$propertiesForm = false;

  self.isSelected = function() {
    return self.task.ui.selected == true;
  }

  self.select = function() {
    self.task.ui.selected = true;
    self.render();
  }

  self.deselect = function() {
    self.task.ui.selected = false;
    self.render();
  }

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
        self.viewport.deselectAllTaskNodes();
        self.select();
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
    var yOffset = (-task.ui.port_radius);
    var index = 0;
    if(!('inputs' in task)) {
      return
    }
    for(var i=0; i<task.inputs.length; i++) {
      var name = task.inputs[i].name
      var src = task.inputs[i].src;
      var key = task.inputs[i].key;
      xOffset += task.ui.port_spacing;
      self.inputPorts.push(new InputPort({
        'name': name,
        'src': src,
        'key': key,
        'svg': self.svg,
        'viewport': self.viewport,
        'taskNode': self.taskNode,
        'taskObj': self,
        'task': self.task,
        'xOffset': xOffset,
        'yOffset': yOffset
      }));
    }
  }

  self.renderOutputPorts = function() {
    self.outputPorts = [];
    var xOffset = task.ui.width;
    var yOffset = (task.ui.height + task.ui.port_radius);
    if(!('outputs' in task)) {
      return
    }
    for(var i=0; i<task.outputs.length; i++) {
      var name = task.outputs[i];
      xOffset -= task.ui.port_spacing;
      self.outputPorts.push(new OutputPort({
        'name': name,
        'svg': self.svg,
        'viewport': self.viewport,
        'taskNode': self.taskNode,
        'taskObj': self,
        'task': self.task,
        'xOffset': xOffset,
        'yOffset': yOffset,
        'index': i
      }));
    }
  }

  self.initPropertiesChangeHandler = function() {
    self.$propertiesForm = self.viewport.$propertiesContainer.find('form');
    self.viewport.showWorkflowProperties();

    self.$propertiesForm.find(':input').on('change', function() {
      var name = $(this).attr('name');
      if(name.indexOf('inputs') >= 0) {
        var field = name.split('-')[1];
        var index = parseInt(name.split('-')[2], 10);
        self.task.inputs[index][field] = $(this).val();
      }
      if(name.indexOf('outputs') >= 0) {
        var index = parseInt(name.split('-')[1], 10);
        self.task.outputs[index] = $(this).val();
      }
      self.render();
      self.viewport.renderConnectors();
    });

    self.$propertiesForm.find('.add-input-properties').on('click', function() {
      self.task.inputs.push({'name': '', 'src': '', 'key': ''});
      self.render();
      self.viewport.renderConnectors();
      return false;
    });

    self.$propertiesForm.find('.add-output-properties').on('click', function() {
      self.task.outputs.push('');
      self.render();
      self.viewport.renderConnectors();
      return false;
    });

    self.$propertiesForm.find('.delete-properties-group').on('click', function() {
      var type = $(this).data('type')
      var index = parseInt($(this).data('index'), 10);
      if(type == 'inputs') {
        self.task.inputs.splice(index, 1);
      }
      if(type == 'outputs') {
        self.task.outputs.splice(index, 1);
      }
      self.render();
      self.viewport.renderConnectors();
      return false;
    });
  }

  self.renderProperties = function() {
    var content = $('#tmpl-task-properties').tmpl({'task': self.task}).html();
    self.viewport.$propertiesContainer.html(content);
    self.initPropertiesChangeHandler();
  }

  self.render = function() {
    self.renderTaskNode();
    self.renderInputPorts();
    self.renderOutputPorts();
    if(self.isSelected()) {
      self.renderProperties();
    }
  }

  self.init = function() {
    self.render();
  }

  self.init();
}

function WorkflowViewPort(identifier, areaIdentifier, workflow) {
  var self = this;
  self.workflow = workflow;
  self.taskNodes = [];
  self.connectors = [];
  self.connectorPaths = [];
  self.$workflowWindow = $(identifier);
  self.$propertiesContainer = $(identifier).find('.workflow-properties');

  self.deselectAllTaskNodes = function() {
    for(var i=0; i<self.taskNodes.length; i++) {
      self.taskNodes[i].deselect();
    }
  }

  self.showWorkflowProperties = function() {
    self.$workflowWindow.addClass('show-workflow-properties');
  }

  self.hideWorkflowProperties = function() {
    self.$workflowWindow.removeClass('show-workflow-properties');
  }

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
    return false;
  }

  self.getOutputPortByKey = function(key) {
    var taskName = key.split('.')[0];
    var portName = key.split('.')[1];
    var taskNode = self.getTaskNodeByName(taskName);
    if(!taskNode) {
      return false;
    }
    for(var i=0; i<taskNode.outputPorts.length; i++) {
      if(portName == taskNode.outputPorts[i].name) {
        return taskNode.outputPorts[i];
      }
    }
    return false
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
        if(inputPort.src == 'taskout') {
          var key = inputPort.key;
          var outputPort = self.getOutputPortByKey(key);
          if(!outputPort) {
            continue;
          }
          self.connectors.push({
            'inputPort': inputPort,
            'outputPort': outputPort
          });
        }
      }
    }
  }

  self.renderPath = function(p1, p2, index) {
    var offset = (index*10) + 15;
    var lineFunction = d3.svg.line()
      .x(function(d) { return d.x; })
      .y(function(d) { return d.y; })
      .interpolate("linear");
    var lineData = [];
    lineData.push(p1);
    lineData.push({x: p1.x+offset, y: p1.y+offset});
    lineData.push({x: (p1.x+p2.x)/2 + offset, y: p1.y+offset});
    lineData.push({x: (p1.x+p2.x)/2 + offset, y: p2.y-offset});
    lineData.push({x: p2.x-offset, y: p2.y-offset});
    lineData.push(p2);

    var path = self.svg.append('path')
      .attr('d', lineFunction(lineData))
      .attr('class', 'task-node-connector');
    return path;
  }

  self.renderConnector = function(p1, p2, index) {
    var path = self.renderPath(p1, p2, index);
    self.connectorPaths.push(path);
  }

  self.renderConnectors = function() {
    for(var i=0; i<self.connectorPaths.length; i++) {
      self.connectorPaths[i].remove();
    }
    self.loadConnectors();
    for(var i=0; i<self.connectors.length; i++) {
      var connector = self.connectors[i];
      var p1 = {
        'x': connector.outputPort.coordinates().x,
        'y': connector.outputPort.coordinates().y
      };
      var p2 = {
        'x': connector.inputPort.coordinates().x,
        'y': connector.inputPort.coordinates().y
      };
      self.renderConnector(p1, p2, connector.outputPort.index);
    }
  }

  self.distanceBetweenPoints = function(p1, p2) {
    return Math.sqrt((p1.x-p2.x)*(p1.x-p2.x) + (p1.y-p2.y)*(p1.y-p2.y));
  }

  self.findNearestInputPort = function(p) {
    var thresholdDistance = 20;
    var nearestPort = false;
    var minDistance = false;
    for(var i=0; i<self.taskNodes.length; i++) {
      var taskNode = self.taskNodes[i];
      for(var j=0; j<taskNode.inputPorts.length; j++) {
        var inputPort = taskNode.inputPorts[j];
        var distance = self.distanceBetweenPoints(p, inputPort.coordinates());
        if(minDistance && distance < minDistance) {
          minDistance = distance;
          nearestPort = inputPort;
        }
        else if(!minDistance){
          minDistance = distance;
          nearestPort = inputPort;
        }
      }
    }
    if(minDistance < thresholdDistance) {
      return {'found': true, 'inputPort': nearestPort};
    }
    return {'found': false};
  }

  self.addConnector = function(outputPort, inputPort) {
    for(var i=0; i<inputPort.task.inputs.length; i++) {
      var input = inputPort.task.inputs[i];
      if(input.name == inputPort.name) {
        input['src'] = 'taskout';
        input['key'] = outputPort.task.name + '.' + outputPort.name;
      }
    }
    inputPort.taskObj.render();
    self.renderConnectors();
  }

  self.init = function() {
    self.svg = d3.select(areaIdentifier)
      .append('svg')
      .attr('width', '100%')
      .attr('height', '100%');
    self.addTasks(self.workflow.tasks);
    self.renderConnectors();

    self.$workflowWindow.on('click', function() {
      self.deselectAllTaskNodes();
      self.hideWorkflowProperties();
    });

    self.$propertiesContainer.on('click', function(event) {
      event.stopPropagation();
    });

    $(document).on('click', '.add-task-button', function(event) {
      event.stopPropagation();
      $('#modal-new-task').modal('show');
      return false;
    });

    $(document).on('submit', '.add-new-task', function() {
      var fields = $(this).serializeArray();
      var task = getEmptyTask();
      for(var i=0; i<fields.length; i++) {
        var field = fields[i];
        task[field.name] = field.value;
      }
      self.addTaskItem(task);
      self.workflow.tasks.push(task);
      $('#modal-new-task').modal('hide');
      $(this).find(':input').each(function() {
        if($(this).attr('type') != 'submit') {
          $(this).val('');
        }
      });
      return false;
    });
  }

  self.init();
}
