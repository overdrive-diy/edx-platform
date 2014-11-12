;(function (define, gettext, undefined) {
    'use strict';
    define(['backbone'], function (Backbone) {
        var NoteItemView = Backbone.View.extend({
            tagName: 'article',
            className: 'edxnotes-page-item',

            initialize: function (options) {
                this.template = _.template($('#note-item-tpl').text());
            },

            render: function () {
                var context = this.model.toContext();
                this.$el.html(this.template(context));
                return this;
            }
        });

        return NoteItemView;
    });
}).call(this, define || RequireJS.define, gettext);
