;(function (define, undefined) {
    'use strict';
    define(['backbone', 'js/edxnotes/views/note_item'],
    function (Backbone, NoteItemView) {
        var RecentActivityView = Backbone.View.extend({
            className: 'edxnotes-page-items-list',

            render: function () {
                this.collection.forEach(function(model) {
                    var item = new NoteItemView({
                        model: model
                    }).render();
                    item.$el.appendTo(this.$el);
                }, this);

                return this;
            }
        });

        return RecentActivityView;
    });
}).call(this, define || RequireJS.define);
