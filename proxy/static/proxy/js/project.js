function addtest(id){
            var str = "<div id='map-"+id+"' >"
                    +"<h4 class='ui teal dividing header'></h4>"
                    +"<div class='two fields'>"
                    +"<div class='required field'>"
                    +"<label>Test Name:</label>"
                    +"<input type='text' name='map-test-"+id+"'></div>"
                    +"<div class='required field'>"
                    +"<label>Automation URL:</label>"
                    +"<input type='text' name='map-url-"+id+"'></div>"
                    +"</div>"
                    +"<div class='two fields'>"
                    +"<div class='field'>"
                    +"<label>Robot Parameters:</label>"
                    +"<input type='text' name='map-robot-"+id+"'></div>"
                    +"<div class='field'>"
                    +"<label>Enable:</label>"
                    +"<div class='ui toggle checkbox'><input type='checkbox' checked='true' name='map-use-"+id+"'><label></label></div></div>"
                    +"</div>"
                    +"<button  class='ui red button'>Delete</button >"
                    +"</div>"
            return str
        };
$(function(){
            $('#testproject').addClass('active');
            var
            $menuItem = $('.menu .item'),
            $dropdown = $('.dropdown'),
            handler = {
                activate: function() {
                    if(!$(this).hasClass('dropdown')) {
                        $(this)
                                .addClass('active')
                                .closest('.ui.menu')
                                .find('.item')
                                .not($(this))
                                .removeClass('active')
                        ;
                    }
                }

            }
            ;
        $menuItem.on('click', handler.activate);
        $dropdown.dropdown('save defaults');
            $('#maps').on('click','.red.button',function(){
            $(this).parent().remove();
            });
            $('#addf').click(function(){
            $('#newtform').find('input').val('');
            $('#newtform').find('.field').removeClass('error');
            $('#newtestproject')
                    .modal({
                        closable:false,
                        onApprove : function() {
                           $("#pageloader").addClass('active');
                                $('#newtform').ajaxSubmit({
                                  url:'/project/add',
                                  success:function(result){
                                    location.href='/';
                                    }
                                })
                        }
                    })
                    .modal('show');
            });
        })
var TestProjectModule=angular.module('TestProjectModule', []);
        TestProjectModule.controller('testpCtrl',['$scope','$http','$compile',
            function($scope,$http,$compile){
                $http.get('/project/getall').success(function(result){
                    $scope.testprojects=result
                });
                $scope.getproject=function(target){
                $('#server_drop').dropdown('clear');
                $('#loader').dimmer("show");
                $('#maps').find(':not(.ng-sope)').remove()
                $('.thirteen.wide.column').css('display','table-cell')
                var $t = angular.element(target);
                $t.siblings().removeClass('active')
                $t.addClass('active blue')
                if ($t.hasClass("header")){
                    id = $t.parent().parent().attr('id')
                    }
                else if ($t[0].tagName=='SPAN')
                    {
                    id = $t.parent().parent().parent().attr('id')
                    }
                else{
                    id = $t.attr('id')
                    }
                testfactory = id
                $.ajax({
                    type:"GET",
                    url:'/project/getdetail',
                    data:{tid:id},
                    success:function(result){
                        $scope.project = result
                        $scope.$apply();
                        $('.dropdown').dropdown();
                        allnode="";
                        for(var node in result.nodes) {
                            $('#server_drop').dropdown('set selected', result.nodes[node].name);
                        }
                        $('#loader').dimmer("hide");
                    }
                });
            };
                $scope.ttladd =function(){
                var mapcount = $('input[name=mapcount]');
                id = mapcount.val();
                if (!id)
                {id=0}
                newmap = addtest(parseInt(id)+1);
                $('#maps').append($compile(newmap)($scope));
                mapcount.val(parseInt(id)+1);
                $scope.$apply();
                };
                $scope.update=function(){
                            $('#loader').dimmer("show");
                            $('#tform').ajaxSubmit({
                              url:'/project/update',
                              success:function(result){
                                $('#loader').dimmer("hide");
                               if (result.status == 'scuess')
                                {
                                    $('#updatemessage .content').html('Update Successful');
                                    $('#updatemessage').modal('show');
                                }
                                else{
                                    $('#updatemessage .content').text(result.status);
                                    $('#updatemessage').modal('show');
                                }
                              }
                              })
               };
               $scope.delete=function(){
                            $('#loader').dimmer("show");
                            $('#tform').ajaxSubmit({
                              url:'/project/delete',
                              success:function(result){
                                $('#loader').dimmer("hide");
                                $('#deletemessage').modal({
                                  closable:false,
                                  onApprove : function() {
                                    location.href='/';
                                  }
                                  }).modal('show');
                                }
                                })
               };
            }
            ]);