;(function (define, gettext, undefined) {
    'use strict';
    define(['jquery', 'underscore', 'backbone', 'date'], function ($, _, Backbone) {
        var NoteItemView = Backbone.View.extend({
            tagName: 'article',
            className: 'edxnotes-item',
            initialize: function (options) {
                this.template = _.template($('#note-item-tpl').text());
            },
            render: function () {
                var context = this.model.toJSON();
                this.$el.html(this.template(context));
                return this;
            }
        });

        return NoteItemView;
    });
}).call(this, define || RequireJS.define, gettext);
